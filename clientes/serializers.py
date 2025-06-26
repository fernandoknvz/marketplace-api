from rest_framework import serializers
from .models import Cliente, ConsultaContacto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'password']

    def create(self, validated_data):
        return Cliente.objects.create(**validated_data)


class ConsultaContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaContacto
        fields = '__all__'
