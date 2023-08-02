from .models import User
from rest_framework import serializers

# Serializers Define Api
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_active', 'groups')

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

