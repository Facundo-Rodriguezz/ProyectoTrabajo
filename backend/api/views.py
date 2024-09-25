from .models import Product
from rest_framework import generics
from .serializers import ProductSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer