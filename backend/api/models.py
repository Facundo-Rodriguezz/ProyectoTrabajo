from django.db import models


class Product(models.Model):  
    nombre = models.CharField(max_length=100)
    description = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')
    stock = models.IntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    objects = models.Manager()


    def __str__(self):
        return str(self.nombre,self.cantidad_disponible)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return str(self.nombre)
