from rest_framework import serializers
from users.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'phone_number', 'bio', 'avatar', 'company_name', 'website', 'favorite_categories')

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'bio', 'avatar', 'company_name', 'website', 'favorite_categories')