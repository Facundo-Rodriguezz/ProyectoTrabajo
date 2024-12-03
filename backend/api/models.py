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
    codigo = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos', default=1)
    eliminado = models.BooleanField(default=False)

    objects = ProductManager()
    objects_all = models.Manager()

    def __str__(self):
        return str(self.nombre, self.cantidad_disponible)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)


class MovimientoStock(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('modificacion', 'Modificacion'),
        ('eliminacion', 'Eliminacion'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movimientos")
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del movimiento
    comentario = models.TextField(blank=True, null=True)  # Por qué se hizo el movimiento (opcional)
    #pylint: disable=no-member

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} - {self.cantidad}"

    def save(self, *args, **kwargs):
        # Lógica para actualizar el stock del producto
        if self.tipo_movimiento == 'entrada':
            self.producto.cantidad += self.cantidad
        elif self.tipo_movimiento == 'salida':
            if self.producto.cantidad >= self.cantidad:
                self.producto.cantidad -= self.cantidad
            else:
                raise ValueError("No hay suficiente stock para esta salida.")

        # Alerta de stock bajo
        if self.producto.cantidad < 10:  # Umbral de alerta (por ejemplo, 10 unidades)
            # Lógica para enviar notificación (correo, SMS, etc.)
            print(f"Alerta: El stock de {self.producto.nombre} es bajo.")  # Aquí puedes implementar una notificación real

        self.producto.save()  # Guardar la nueva cantidad en el producto
        super().save(*args, **kwargs)


# Signals

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    # Crear un movimiento de stock de tipo 'entrada' cuando se crea un nuevo producto
    if kwargs['created']:
        MovimientoStock.objects.create(
            producto=instance,
            tipo_movimiento='entrada',
            cantidad=instance.cantidad_disponible,
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
                tipo_movimiento='entrada',
                cantidad=instance.cantidad_disponible - old_product.cantidad_disponible,
                comentario='Actualización de cantidad disponible'
            )
        elif old_product.stock != instance.stock:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='entrada',
                cantidad=instance.cantidad_disponible,
                comentario='Actualización de stock'
            )
        elif old_product.precio != instance.precio:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad=instance.cantidad_disponible,
                comentario='Actualización de precio'
            )
        elif old_product.nombre != instance.nombre:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad=instance.cantidad_disponible,
                comentario='Actualización de nombre'
            )
        elif old_product.categoria != instance.categoria:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad=instance.cantidad_disponible,
                comentario='Actualización de categoria'
            )
        elif old_product.descripcion != instance.descripcion:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='modificacion',
                cantidad=instance.cantidad_disponible,
                comentario='Actualización de descripcion'
            )
        elif old_product.eliminado != instance.eliminado:
            MovimientoStock.objects.create(
                producto=instance,
                tipo_movimiento='eliminacion',
                cantidad=instance.cantidad_disponible,
                comentario='Eliminación de producto'
            )
        else:
            pass
