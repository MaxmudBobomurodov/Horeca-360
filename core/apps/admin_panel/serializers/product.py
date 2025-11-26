from rest_framework import serializers

from core.apps.products.models import Product


class AdminProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'category', 'price', 'description', 'unity', 'tg_id', 'quantity_left', 'min_quantity'
        ]

    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'image', 'category', 'price', 'description', 'unity', 'tg_id',
            'quantity_left', 'min_quantity'
        ]
        extra_kwargs = {
            'image': {'required': False},
            'category': {'required': False},
            'price': {'required': False},
            'tg_id': {'required': False},
            'quantity_left': {'required': False},
        }
