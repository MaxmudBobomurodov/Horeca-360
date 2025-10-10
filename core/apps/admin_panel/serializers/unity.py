from rest_framework import serializers

from core.apps.products.models import Unity


class UnitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Unity
        fields = [
            'id', 'name',
        ]