from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito, ItemCarrito
from productos.models import Producto

class CarritoListAPIView(APIView):
    def get(self, request):
        carrito, _ = Carrito.objects.get_or_create(id=1)  # para simplificar en test
        items = ItemCarrito.objects.filter(carrito=carrito)
        data = [{'producto': item.producto.nombre, 'cantidad': item.cantidad} for item in items]
        return Response({'items': data})

class AgregarItemCarritoAPIView(APIView):
    def post(self, request):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        carrito, _ = Carrito.objects.get_or_create(id=1)  # para simplificar en test
        item = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return Response({
            'producto': item.producto.nombre,
            'cantidad': item.cantidad
        }, status=status.HTTP_201_CREATED)
