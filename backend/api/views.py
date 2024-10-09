from .models import Product
from .models import MovimientoStock
from .serializers import ProductSerializer,UserSerializer, MovimientoStockSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Esto levantará un error si la validación falla
        self.perform_create(serializer)  # Guarda el objeto
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
            return [IsAdminUser()]
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovimientoStockViewSet(viewsets.ModelViewSet):
    # pylint: disable=no-member
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer

    
