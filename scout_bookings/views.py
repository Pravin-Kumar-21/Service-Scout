from rest_framework import generics, permissions
from .models import ServiceBooking
from scout_bookings.BookingSerilaizers import ServiceBookingSerializer
from scout_users.models import Customer, ServiceProvider
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class IsCustomerOrProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.customer.user == request.user or
            obj.service_provider.user == request.user
        )

class CustomerBookingListView(generics.ListAPIView):
    serializer_class = ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = get_object_or_404(Customer, id=self.kwargs['customer_id'], user=self.request.user)
        return ServiceBooking.objects.filter(customer=customer)

class ProviderBookingListView(generics.ListAPIView):
    serializer_class = ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        provider = get_object_or_404(ServiceProvider, id=self.kwargs['provider_id'], user=self.request.user)
        return ServiceBooking.objects.filter(service_provider=provider)

class ServiceBookingDetailView(generics.RetrieveAPIView):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer
    lookup_field = 'service_booking_uuid'
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrProvider]

class ServiceBookingDeleteView(generics.DestroyAPIView):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer
    lookup_field = 'service_booking_uuid'
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrProvider]

class CreateServiceBookingView(generics.CreateAPIView):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            customer = Customer.objects.get(user=self.request.user)
        except Customer.DoesNotExist:
            raise ValidationError("Only customers can book a service.")

        service = serializer.validated_data.get('service_name')
        if not service:
            raise ValidationError("Service is required and must be valid.")

        service_provider = service.provider  # fixed here

        serializer.save(customer=customer, service_provider=service_provider)
