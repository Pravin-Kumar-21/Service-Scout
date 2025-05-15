from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "user_type",
                    "country_code",
                    "state",
                    "city",
                    "address",
                    "phone_number",
                    "is_verified",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",         # <-- include email
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_filter = UserAdmin.list_filter + (
        "user_type",
        "is_verified",
        "state",
        "city",
    )
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "user_uuid",
        "email",
        "user_type",
        "is_verified",
        "is_active",
        "is_staff",
    )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for Customer Profiles"""

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "preferred_language",
        "subscription_plan",
        "subscription_status",
        "profile_completion",
    )
    list_filter = (
        "subscription_plan",
        "subscription_status",
        "preferred_language",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "referral_code",
    )


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    """Admin for Service Provider Profiles"""

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    list_display = (
        "username",
        "email",
        "service_name",
        "availability_status",
        "verification_status",
        "total_completed_jobs",
        "user_rating",
    )
    list_filter = (
        "availability_status",
        "verification_status",
        "service_location",
    )
    search_fields = (
        "user__username",
        "user__email",
        "service_name",
        "user_description",
    )
