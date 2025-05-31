# carrito/views.py
from ventas.models import OrdenVenta, DetalleVenta
from django.db import transaction  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito, ItemCarrito
from .serializers import AgregarItemCarritoSerializer, ItemCarritoSerializer
from productos.models import Producto
from rest_framework import viewsets
from .serializers import CarritoSerializer
from productos.models import Precio

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer


class AgregarAlCarritoView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AgregarItemCarritoSerializer(data=request.data)
        if serializer.is_valid():
            producto = Producto.objects.get(id=serializer.validated_data['producto_id'])
            cantidad = serializer.validated_data['cantidad']

            # Obtener o crear el carrito del usuario (versión simple)
            carrito, created = Carrito.objects.get_or_create(pk=1, defaults={})

            # Verificar si el item ya existe en el carrito
            item, creado = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={'cantidad': cantidad}
            )

            if not creado:
                item.cantidad += cantidad
                item.save()

            # Serializar el contenido actualizado del carrito
            items = ItemCarrito.objects.filter(carrito=carrito)
            items_data = ItemCarritoSerializer(items, many=True).data

            return Response({
                "mensaje": "Producto agregado al carrito",
                "carrito": items_data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerCarritoView(APIView):
    def get(self, request, *args, **kwargs):
        carrito = Carrito.objects.get(pk=1)  # Versión simple: carrito global
        items = ItemCarrito.objects.filter(carrito=carrito)

        resultado = []
        total = 0

        for item in items:
            # Obtener el precio más reciente
            precio = Precio.objects.filter(producto=item.producto).order_by('-fecha').first()
            precio_valor = precio.valor if precio else 0

            subtotal = item.cantidad * precio_valor
            total += subtotal

            resultado.append({
                "producto_id": item.producto.id,
                "producto": item.producto.nombre,
                "cantidad": item.cantidad,
                "precio_unitario": precio_valor,
                "subtotal": subtotal
            })

        return Response({
            "carrito": resultado,
            "total": total
        }, status=status.HTTP_200_OK)
    



class ConfirmarCompraView(APIView):
    def post(self, request, *args, **kwargs):
        cliente_id = request.data.get("cliente_id")
        empleado_id = request.data.get("empleado_id")

        if not cliente_id or not empleado_id:
            return Response({"error": "cliente_id y empleado_id son requeridos"}, status=400)

        try:
            carrito = Carrito.objects.get(pk=1)
            items = ItemCarrito.objects.filter(carrito=carrito)
            if not items.exists():
                return Response({"error": "El carrito está vacío"}, status=400)

            with transaction.atomic():
                orden = OrdenVenta.objects.create(
                    cliente_id=cliente_id,
                    empleado_id=empleado_id
                )

                total = 0
                for item in items:
                    precio = Precio.objects.filter(producto=item.producto).order_by("-fecha").first()
                    precio_unitario = precio.valor if precio else 0
                    subtotal = item.cantidad * precio_unitario
                    total += subtotal

                    DetalleVenta.objects.create(
                        orden_id=orden.id,
                        producto_id=item.producto.id,
                        cantidad=item.cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal
                    )

                    # Reducir stock
                    item.producto.stock -= item.cantidad
                    item.producto.save()

                # Vaciar carrito
                ItemCarrito.objects.all().delete()


            return Response({"mensaje": "Compra confirmada", "orden_id": orden.id, "total": total})

        except Carrito.DoesNotExist:
            return Response({"error": "No existe carrito"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class VaciarCarritoView(APIView):
    def post(self, request):
        try:
            carrito = Carrito.objects.get(pk=1)  # asumimos 1 como carrito actual
            ItemCarrito.objects.filter(carrito=carrito).delete()
            return Response({"mensaje": "Carrito vaciado correctamente"}, status=status.HTTP_200_OK)
        except Carrito.DoesNotExist:
            return Response({"error": "Carrito no encontrado"}, status=status.HTTP_404_NOT_FOUND)
