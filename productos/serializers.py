from .models import Producto, Precio, Categoria
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    precio_actual = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'nombre', 'marca', 'stock', 'categoria', 'categoria_nombre', 'precio_actual', 'imagen_url']

    def get_precio_actual(self, obj):
        ultimo_precio = Precio.objects.filter(producto=obj).order_by('-fecha').first()
        if ultimo_precio:
            return {
                'valor': ultimo_precio.valor,
                'fecha': ultimo_precio.fecha
            }
        return None


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']
