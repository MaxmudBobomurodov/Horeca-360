import math
from django.db import transaction
from rest_framework import serializers

from core.apps.orders.models import Order, OrderItem
from core.apps.products.models import Product
from core.apps.products.serializers.product import ProductListSerializer
from core.apps.orders.tasks.order_item import send_orders_to_tg_bot, send_message_order_user


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.FloatField()

    def validate(self, data):
        product = Product.objects.filter(id=data['product_id']).first()
        if not product:
            raise serializers.ValidationError("Product not found")

        data['product'] = product

        if data.get('object_id'):
            from core.apps.products.models import Object
            obj = Object.objects.filter(id=data['object_id']).first()
            if not obj:
                raise serializers.ValidationError("Object not found")
            data['object'] = obj

        product.quantity_left -= round(data['quantity'] / product.min_quantity)
        product.save()

        data['price'] = round((data['quantity'] / product.min_quantity) * product.price)
        return data


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    comment = serializers.CharField(required=False)

    def create(self, validated_data):
        with transaction.atomic():
            order_items = validated_data.pop('items')
            order = Order.objects.create(
                user=self.context.get('user'),
                comment=validated_data.get('comment')
            )

            items = []
            total_price = 0

            for item in order_items:
                product = item.get("product")
                items.append(OrderItem(
                    product=product,
                    price=item.get('price'),
                    quantity=item.get('quantity'),
                    order=order,
                    object=item.get('object'),
                ))
                total_price += item['price']

                send_orders_to_tg_bot.delay(
                    chat_id=item.get('product').tg_id,
                    product_name=item.get('product').name,
                    quantity=item.get('quantity'),
                    username=order.user.username,
                )

            OrderItem.objects.bulk_create(items)
            order.total_price = total_price
            order.save()

            send_message_order_user.delay(
                chat_id=order.user.tg_id,
                order_id=order.id,
            )
            return order


class OrderItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'price', 'quantity', 'created_at'
        ]

    def get_product(self, obj):
        serializer = ProductListSerializer(obj.product, context=self.context)
        return serializer.data


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_price',
            'comment', 'items', 'created_at'
        ]
