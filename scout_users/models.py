# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """Base user model."""
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    USER_TYPE = (
        ('customer', 'Customer'),
        ('service_provider', 'Service Provider'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    user_uuid = models.UUIDField(
      default=uuid.uuid4, unique=True, editable=False
      )
    gender = models.CharField(
      max_length=50, choices=GENDER_CHOICES,
      default='other', null=True, blank=True
      )

    def photo_profile_path_location(instance, filename):
        return f'profile_pictures/{instance.username}/{filename}'

    profile_picture = models.ImageField(
      upload_to=photo_profile_path_location, null=True, blank=True
      )
    country_code = models.CharField(
      max_length=10, null=True, blank=True, verbose_name='Country Code'
      )
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(
      max_length=50, choices=USER_TYPE, null=True, blank=True
      )
    
    REQUIRED_FIELDS = [
      "email",
    ]

    def __str__(self):
        return self.email


class Customer(models.Model):

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='customer_profile'
      )

    preferred_language = models.CharField(max_length=50, null=True, blank=True)
    subscription_plan = models.CharField(max_length=50, null=True, blank=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    subscription_status = models.BooleanField(default=False)
    profile_completion = models.IntegerField(default=0)
    user_rating = models.FloatField(default=0.0, null=True, blank=True)
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.user.user_type = 'customer'
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email}'


class ServiceProvider(models.Model):

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"

    user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='service_provider_profile'
      )

    AVAILABILITY = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    )
    VERIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    user_description = models.TextField(null=True, blank=True)
    user_rating = models.FloatField(default=0.0, null=True, blank=True)
    user_rating_count = models.IntegerField(default=0, null=True, blank=True)
    service_name = models.CharField(max_length=50, null=True, blank=True)
    service_description = models.TextField(null=True, blank=True)
    work_experience = models.IntegerField(null=True, blank=True)
    availability_status = models.CharField(
      max_length=50, choices=AVAILABILITY, default='available'
      )
    service_location = models.CharField(max_length=100, null=True, blank=True)
    total_completed_jobs = models.IntegerField(null=True, blank=True)
    required_documents = models.CharField(
      max_length=255, null=True, blank=True
      )
    document_verification_status = models.BooleanField(default=False)
    verification_status = models.CharField(
      max_length=50, choices=VERIFICATION_STATUS, default='pending'
      )

    def service_provider_document_path(instance, filename):
        return f'documents/{instance.user.user_uuid}/{filename}'

    def service_provider_portfolio_path(instance, filename):
        return f'portfolio/{instance.user.user_uuid}/{filename}'

    user_verified_documents = models.FileField(
      upload_to=service_provider_document_path, null=True, blank=True
      )
    portfolio_images = models.ImageField(
      upload_to=service_provider_portfolio_path, null=True, blank=True
      )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.user.user_type = 'service_provider'
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email}'
