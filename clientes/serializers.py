from rest_framework import serializers
from .models import Cliente

class ClienteRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'password']

    def create(self, validated_data):
        return Cliente.objects.create(**validated_data)
