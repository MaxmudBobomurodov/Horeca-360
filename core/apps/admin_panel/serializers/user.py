from django.db import transaction

from rest_framework import serializers

from core.apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'last_login', 'date_joined', 'is_superuser',
        ]
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data.get('username'),
                is_superuser=validated_data.get('is_superuser')
            )
            user.set_password(validated_data.get('password'))
            user.save()
            return user
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.username = validated_data.get('username', instance.username)
            if validated_data.get('password'):
                instance.set_password(validated_data.get('password'))
            instance.save()
            return instance
        

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username'], is_superuser=True).first()
        if not user:
            raise serializers.ValidationError("User not found")
        data['user'] = user
        return data