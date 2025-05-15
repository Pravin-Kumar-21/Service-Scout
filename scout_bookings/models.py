import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime
from scout_users.models import Customer, ServiceProvider
from scout_services.models import ScoutServices

class ServiceBooking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service_booking_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    service_name = models.ForeignKey(ScoutServices, on_delete=models.CASCADE, related_name='booked_services')
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField(help_text="Service address or location details")
    special_instructions = models.TextField(blank=True, null=True, help_text="Any extra notes from the customer")
    is_paid = models.BooleanField(default=False)
    auto_cancel_time = models.DateTimeField(blank=True, null=True, help_text="Optional: cancel if not confirmed by this time")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Booking'
        verbose_name_plural = 'Service Bookings'

    def __str__(self):
        return f"{self.customer} booked {self.service_name} with {self.service_provider} on {self.booking_date} at {self.booking_time}"

    def is_upcoming(self):
        booking_datetime = timezone.make_aware(datetime.combine(self.booking_date, self.booking_time))
        return booking_datetime > timezone.now()

    def auto_cancel_if_needed(self):
        if self.status == self.STATUS_PENDING and self.auto_cancel_time and timezone.now() > self.auto_cancel_time:
            self.status = self.STATUS_CANCELLED
            self.save()

    def save(self, *args, **kwargs):
        if not self.service_provider:
            self.service_provider = self.service_name.provider  # fixed field name here
        super().save(*args, **kwargs)
