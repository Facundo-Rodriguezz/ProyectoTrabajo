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

def cargar_productos():
    productos = [
        {
            'nombre': 'Producto 1',
            'descripcion': 'Descripción 1',
            'cantidad_disponible': 10,
            'stock': 50,  
            'precio': 100.00
        },
        {
            'nombre': 'Producto 2',
            'descripcion': 'Descripción 2',
            'cantidad_disponible': 20,
            'stock': 100, 
            'precio': 200.00
        },
        
    ]

    for p in productos:
        Product.objects.create(**p)

from rest_framework.decorators import api_view

@api_view(['GET'])
def obtener_datos(_):
    data = {"message": "Datos desde Django Rest Framework"}
    return Response(data)




