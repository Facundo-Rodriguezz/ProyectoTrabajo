from django.db import models


class Product(models.Model):
    nombre = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True, blank=True)
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, null=True)
    descripcion = models.TextField(null=True)  # Ahora es opcional
    


    def __str__(self):
        return str(self.nombre)


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
