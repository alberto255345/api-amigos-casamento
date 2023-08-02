from .models import User#, categoryUser
from rest_framework import serializers

# Serializers Define Api
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'category', 'Active')

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = categoryUser
#         fields = ('id', 'category')


