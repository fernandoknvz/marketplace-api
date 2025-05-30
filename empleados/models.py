from django.db import models

class Empleado(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20)

    class Meta:
        db_table = 'empleado'
        managed = False  

    def __str__(self):
        return self.username
