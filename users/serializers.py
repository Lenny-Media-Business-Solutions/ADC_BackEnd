from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'is_active', 'is_staff', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
