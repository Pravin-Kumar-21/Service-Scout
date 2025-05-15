from rest_framework import serializers
from .models import ServiceBooking

class ServiceBookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)
    service_name_text = serializers.CharField(source='service_name.service_name', read_only=True)  # fixed field name
    provider_name = serializers.CharField(source='service_provider.user.username', read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = ServiceBooking
        fields = [
            'id',
            'customer',
            'customer_name',
            'service_provider',
            'provider_name',
            'service_name',
            'service_name_text',
            'status',
            'booking_date',
            'booking_time',
            'created_at',
            'updated_at',
            'address',
            'special_instructions',
            'is_paid',
            'auto_cancel_time',
            'progress'
        ]
        read_only_fields = [
            'customer', 'service_provider',
            'created_at', 'updated_at', 'progress',
            'customer_name', 'provider_name', 'service_name_text'
        ]

    def get_progress(self, obj):
        # Using is_upcoming method from the model as progress example
        return obj.is_upcoming()
