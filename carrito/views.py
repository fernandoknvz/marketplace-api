from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito, ItemCarrito
from productos.models import Producto
from precios.models import Precio

class CarritoListAPIView(APIView):
    def get(self, request):
        carrito, _ = Carrito.objects.get_or_create(id=1)
        items = ItemCarrito.objects.filter(carrito=carrito)

        total = 0
        items_data = []

        for item in items:
            precio = Precio.objects.filter(producto=item.producto).order_by('-fecha').first()
            if not precio:
                valor_unitario = 0
            else:
                valor_unitario = precio.valor

            subtotal = valor_unitario * item.cantidad
            total += subtotal

            items_data.append({
                'producto_id': item.producto.id,
                'producto': item.producto.nombre,
                'cantidad': item.cantidad,
                'valor_unitario': float(valor_unitario),
                'subtotal': float(subtotal)
            })

        return Response({
            'items': items_data,
            'total': float(total)
        })
class AgregarItemCarritoAPIView(APIView):
    def post(self, request):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        carrito, _ = Carrito.objects.get_or_create(id=1)  
        item = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return Response({
            'producto': item.producto.nombre,
            'cantidad': item.cantidad
        }, status=status.HTTP_201_CREATED)

class VaciarCarritoAPIView(APIView):
    def post(self, request):
        carrito, _ = Carrito.objects.get_or_create(id=1)
        carrito.items.all().delete()
        return Response({'mensaje': 'Carrito vaciado correctamente'}, status=status.HTTP_200_OK)

class ActualizarItemCarritoAPIView(APIView):
    def post(self, request):
        producto_id = request.data.get('producto_id')
        nueva_cantidad = request.data.get('cantidad')

        if not producto_id or not nueva_cantidad:
            return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
            carrito = Carrito.objects.get(id=1)
            item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
            item.cantidad = nueva_cantidad
            item.save()
            return Response({'mensaje': 'Cantidad actualizada'}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no existe'}, status=status.HTTP_404_NOT_FOUND)
        except ItemCarrito.DoesNotExist:
            return Response({'error': 'Item no existe en el carrito'}, status=status.HTTP_404_NOT_FOUND)

class EliminarItemCarritoAPIView(APIView):
    def post(self, request):
        producto_id = request.data.get('producto_id')
        try:
            carrito = Carrito.objects.get(id=1)
            producto = Producto.objects.get(id=producto_id)
            item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
            item.delete()
            return Response({'mensaje': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
        except (Producto.DoesNotExist, ItemCarrito.DoesNotExist):
            return Response({'error': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)
