from rest_framework import serializers
from .models import OrdenVenta, DetalleVenta, Cliente
from productos.models import Producto, Precio
from rest_framework import serializers
from .models import OrdenVenta

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class DetalleVentaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()


class OrdenVentaCreateSerializer(serializers.Serializer):
    cliente_email = serializers.EmailField()
    productos = DetalleVentaSerializer(many=True)

    def create(self, validated_data):
        try:
            cliente = Cliente.objects.get(email=validated_data.get('cliente_email'))
        except Cliente.DoesNotExist:
            raise serializers.ValidationError(f"No existe un cliente con email {validated_data.get('cliente_email')}")

        orden = OrdenVenta.objects.create(cliente=cliente)

        for item in validated_data['productos']:
            producto = Producto.objects.get(id=item['producto_id'])

            # Obtener el precio más reciente del producto
            precio = Precio.objects.filter(producto_id=producto.id).order_by('-fecha').first()
            if not precio:
                raise serializers.ValidationError(f"No hay precio disponible para el producto {producto.nombre}")

            DetalleVenta.objects.create(
                orden=orden,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=precio.valor
            )

        return orden


class DetalleVentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class OrdenVentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaModelSerializer(many=True, read_only=True)

    class Meta:
        model = OrdenVenta
        fields = '__all__'


class SimularPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenVenta
        fields = ['id', 'estado_pago']
