from .models import Categoria, Product
from .models import MovimientoStock
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, MovimientoStockSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.db.models import Count


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
        if self.action in ['crear', 'actualizar', 'destruir']:
            self.permission_classes = [IsAdminUser]  # Solo admin puede crear, actualizar o destruir
        else:
            self.permission_classes = [IsAuthenticated]  # Para las otras acciones, solo autenticados
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovimientoStockViewSet(viewsets.ModelViewSet):
    # pylint: disable=no-member
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        enviar_cantidades = self.request.query_params.get('enviar_cantidades', None)
        if enviar_cantidades:
            return Categoria.objects.annotate(cantidad_productos=Count('productos'))
        return super().get_queryset()


@api_view(['GET'])
def obtener_datos(_):
    data = {"message": "Datos desde Django Rest Framework"}
    return Response(data)
