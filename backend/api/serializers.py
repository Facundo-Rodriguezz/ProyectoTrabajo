from .models import Categoria, Product
from .models import MovimientoStock
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class ProductSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Product
        fields = '__all__'


class MovimientoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoStock
        fields = ['producto', 'tipo_movimiento', 'cantidad', 'comentario']

    def validate(self, attrs):
        producto = attrs['producto']
        cantidad = attrs['cantidad']
        tipo_movimiento = attrs['tipo_movimiento']

        if tipo_movimiento == 'salida' and producto.cantidad < cantidad:
            raise serializers.ValidationError("No hay suficiente stock disponible.")

        return attrs


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if hasattr(instance, 'cantidad_productos'):
            ret['cantidad_productos'] = instance.cantidad_productos

        return ret
