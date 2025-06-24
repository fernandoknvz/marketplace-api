from django.db import models
from productos.models import Producto
# Create your models here.


class Carrito(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
