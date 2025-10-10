from rest_framework import serializers

from core.apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'image', 'order'
        ]
