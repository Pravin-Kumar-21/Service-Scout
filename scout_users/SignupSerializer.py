from .models import Customer, ServiceProvider
from rest_framework import serializers
from django.contrib.auth import get_user_model
from scout_users.serializers import UserSerializer
User = get_user_model()

class CustomerSignupSerializer(serializers.ModelSerializer):
    # Nest user data
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'preferred_language', 'subscription_plan')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class ServiceProviderSignupSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ServiceProvider
        fields = ('id', 'user', 'service_name', 'work_experience', 'service_description')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        provider = ServiceProvider.objects.create(user=user, **validated_data)
        return provider
