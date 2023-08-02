from .models import User, Photo
from rest_framework import serializers

# Serializers Define Api
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_active', 'groups')

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'created_at')
