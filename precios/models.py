from django.db import models
from productos.models import Producto

class Precio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'precios'

    def __str__(self):
        return f"{self.producto.nombre} - {self.valor} ({self.fecha})"
