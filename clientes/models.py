from django.db import models
import sys

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'cliente'
        managed = not 'test' in sys.argv

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ConsultaContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consultas_contacto'

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
