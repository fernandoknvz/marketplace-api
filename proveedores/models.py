# proveedores/models.py

from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'proveedores'

    def __str__(self):
        return self.nombre
