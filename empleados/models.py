from django.db import models

class Empleado(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, null=True, blank=True)
    rol = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleado'

    def __str__(self):
        return self.username
