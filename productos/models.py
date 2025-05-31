from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    imagen_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre


class Precio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'precios'

    def __str__(self):
        return f"{self.producto.nombre} - {self.valor} ({self.fecha})"
    
