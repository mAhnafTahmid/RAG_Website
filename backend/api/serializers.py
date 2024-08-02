from django.contrib.auth.models import User
from rest_framework import serializers
from .models import QA


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ["id", "ai", "message", "created_at", "user"]
        extra_kwargs = {
            "user": {"read_only": True},
            "ai": {"required": False},
        }
