from django.contrib import admin
from .models import ServiceBooking

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'service_provider', 'service_booking_uuid' ,  'service_name',
        'booking_date', 'booking_time', 'status', 'is_paid', 'created_at'
    )
    list_filter = ('status', 'is_paid', 'booking_date')
    search_fields = ('customer__user__username', 'service_provider__user__username', 'service_name__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'auto_cancel_time')
