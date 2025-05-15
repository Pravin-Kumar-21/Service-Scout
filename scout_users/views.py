from django.shortcuts import render
from scout_users.models import User, Customer, ServiceProvider
from scout_users.serializers import UserSerializer
from scout_users.SignupSerializer import CustomerSignupSerializer, ServiceProviderSignupSerializer


from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

# Create your views here.


class CustomerSignupView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSignupSerializer


class ServiceProviderSignupView(generics.CreateAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSignupSerializer


class UserDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve user details.
    Only accessible to authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently logged-in user (from the request)
        print(self.request.user.pk)
        return self.request.user


class CustomerUserUpdateView(generics.UpdateAPIView):
    """
    API view to update customer user details.
    Only accessible to authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently logged-in user (from the request)
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=HTTP_200_OK)


class ServiceProviderUserUpdateView(generics.UpdateAPIView):
    """
    API view to update service provider user details.
    Only accessible to authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently logged-in user (from the request)
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=HTTP_200_OK)
