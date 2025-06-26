from rest_framework import serializers
from .models import Producto
from precios.models import Precio

class ProductoSerializer(serializers.ModelSerializer):
    precio_actual = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'nombre', 'marca', 'stock', 'categoria', 'imagen_url', 'precio_actual']

    def get_precio_actual(self, obj):
        precio = Precio.objects.filter(producto=obj).order_by('-fecha').first()
        if precio:
            return {
                'valor': precio.valor,
                'fecha': precio.fecha
            }
        else:
            return None
