from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.accounts.models import User
from core.apps.products.models import Product


class Order(BaseModel):
    total_price = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.PositiveBigIntegerField(default=1)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'Buyurtma #{self.order_number} - {self.user}'

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.FloatField()
    price = models.PositiveBigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', null=True)

    def __str__(self):
        return f'{self.quantity} x {self.product} ({self.price})'

    class Meta:
        verbose_name = 'Buyurtma elementi'
        verbose_name_plural = 'Buyurtma elementlari'
