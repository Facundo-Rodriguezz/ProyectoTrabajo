from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(eliminado=False)


class Product(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()
    eliminado = models.BooleanField(default=False)
    codigo = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos', default=1)
    objects = ProductManager()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.nombre, self.cantidad_disponible)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)


class MovimientoStock(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movimientos")
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad_disponible = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del movimiento
    comentario = models.TextField(blank=True, null=True)  # Por qué se hizo el movimiento (opcional)
    #pylint: disable=no-member

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} - {self.cantidad_disponible}"


# Signals
@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    # Crear un movimiento de stock de tipo 'entrada' cuando se crea un nuevo producto
    if kwargs['created']:
        MovimientoStock.objects.create(
            producto=instance,
            tipo_movimiento='entrada',
            cantidad_disponible=instance.cantidad_disponible,
            comentario='Creación de nuevo producto'
        )


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    # Crear un movimiento de stock de tipo 'entrada' cuando se actualiza la cantidad disponible de un producto
    if instance.pk:
        old_product = Product.objects.get(pk=instance.pk)
        if old_product.cantidad_disponible != instance.cantidad_disponible:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad_disponible=instance.cantidad_disponible - old_product.cantidad_disponible,
                comentario='Actualización de cantidad disponible'
            )
        elif old_product.precio != instance.precio:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad_disponible=instance.cantidad_disponible,
                comentario='Actualización de precio'
            )
        elif old_product.nombre != instance.nombre:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad_disponible=instance.cantidad_disponible,
                comentario='Actualización de nombre'
            )
        elif old_product.categoria != instance.categoria:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad_disponible=instance.cantidad_disponible,
                comentario='Actualización de categoria'
            )
        elif old_product.eliminado != instance.eliminado:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='eliminacion',
                cantidad_disponible=instance.cantidad_disponible,
                comentario='Eliminación de producto'
            )
        else:
            pass
