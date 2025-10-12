from rest_framework import serializers

from core.apps.products.models import Object


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = [
            'id', 'name',
        ]