from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'cliente'
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
