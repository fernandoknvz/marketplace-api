from django.db import models
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class RegistroClienteView(APIView):
    def post(self, request):
        data = request.data
        try:
            cliente = Cliente.objects.create(
                nombre=data["nombre"],
                apellido=data["apellido"],
                email=data["email"],
                password=data["password"]  # puedes encriptar más adelante
            )
            return Response({
                "mensaje": "Cliente registrado exitosamente",
                "id": cliente.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)