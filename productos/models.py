from django.db import models

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField()
    categoria = models.ForeignKey('categorias.Categoria', on_delete=models.CASCADE, null=True, blank=True)
    imagen_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre


