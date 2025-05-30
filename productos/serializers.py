from rest_framework import serializers
from .models import Producto, Precio
from datetime import date

class ProductoSerializer(serializers.ModelSerializer):
    precio_inicial = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )

    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'nombre', 'marca', 'stock', 'categoria', 'precio_inicial']

    def create(self, validated_data):
        precio_valor = validated_data.pop('precio_inicial')
        producto = Producto.objects.create(**validated_data)
        Precio.objects.create(producto=producto, fecha=date.today(), valor=precio_valor)
        return producto
