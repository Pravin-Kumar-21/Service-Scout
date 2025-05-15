from django.urls import path
from .views import (
    CustomerBookingListView,
    ProviderBookingListView,
    ServiceBookingDetailView,
    ServiceBookingDeleteView,
    CreateServiceBookingView,
)

urlpatterns = [
    path('users/bookings/', CustomerBookingListView.as_view(), name='customer-bookings-list'),
    path('users/bookings/<str:service_booking_uuid>/', ServiceBookingDetailView.as_view(), name='customer-bookings-detail'),
    path('bookings/create/', CreateServiceBookingView.as_view(), name='booking-create'),
    path('providers/<int:provider_id>/bookings/', ProviderBookingListView.as_view(), name='provider-bookings-list'),
    path('bookings/<str:service_booking_uuid>/delete/', ServiceBookingDeleteView.as_view(), name='booking-delete'),
]
