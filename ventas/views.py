from rest_framework import viewsets
from .models import Cliente, OrdenVenta, DetalleVenta
from .serializers import ClienteSerializer, OrdenVentaSerializer, DetalleVentaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenVentaCreateSerializer
from .models import OrdenVenta, DetalleVenta, Cliente, Empleado
from precios.models import Precio
from carrito.models import Carrito, ItemCarrito
import requests
from .utils import obtener_dolar_a_clp


class RegistrarVentaAPIView(APIView):
    def post(self, request):
        serializer = OrdenVentaCreateSerializer(data=request.data)
        if serializer.is_valid():
            orden = serializer.save()
            return Response({"mensaje": f"Orden #{orden.id} registrada correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class OrdenVentaViewSet(viewsets.ModelViewSet):
    queryset = OrdenVenta.objects.all()
    serializer_class = OrdenVentaSerializer


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class RegistrarVentaAPIView(APIView):
    def post(self, request):
        serializer = OrdenVentaCreateSerializer(data=request.data)
        if serializer.is_valid():
            orden = serializer.save()
            return Response({"mensaje": f"Orden #{orden.id} registrada correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SimularPagoView(APIView):
    def post(self, request, pk):
        try:
            orden = OrdenVenta.objects.get(pk=pk)
        except OrdenVenta.DoesNotExist:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        orden.estado_pago = "pagado"
        orden.save()

        return Response({
            "mensaje": "Pago simulado exitosamente",
            "orden_id": orden.id,
            "estado_pago": orden.estado_pago
        }, status=status.HTTP_200_OK)
    

class ValorDolarAPIView(APIView):
    def get(self, request):
        try:
            response = requests.get("https://api.frankfurter.app/latest?from=USD&to=CLP")
            data = response.json()
            return Response({
                "moneda_origen": "USD",
                "moneda_destino": "CLP",
                "valor": data["rates"]["CLP"],
                "fecha": data["date"]
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TasaCambioView(APIView):
    def get(self, request):
        valor = obtener_dolar_a_clp()
        if valor is not None:
            return Response({"usd_to_clp": valor}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No se pudo obtener la tasa de cambio"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class DetalleOrdenAPIView(APIView):
    def get(self, request, pk):
        try:
            orden = OrdenVenta.objects.get(pk=pk)
            detalles = DetalleVenta.objects.filter(orden=orden)

            resultado = []
            total = 0

            for item in detalles:
                subtotal = item.cantidad * item.precio_unitario
                total += subtotal
                resultado.append({
                    "producto": item.producto.nombre,
                    "cantidad": item.cantidad,
                    "precio_unitario": item.precio_unitario,
                    "subtotal": subtotal
                })

            return Response({
                "detalle": resultado,
                "total": total
            })

        except OrdenVenta.DoesNotExist:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ConfirmarPagoView(APIView):
    def post(self, request):
        data = request.data
        try:
            cliente = Cliente.objects.get(id=data["cliente_id"])
            empleado = Empleado.objects.get(id=data["empleado_id"])
            metodo = data.get("metodo_pago", "Tarjeta")

            carrito = Carrito.objects.filter(cliente=cliente).latest('fecha_creacion')
            items = ItemCarrito.objects.filter(carrito=carrito)

            if not items.exists():
                return Response({"error": "El carrito está vacío"}, status=400)

            # 2. Crear la orden
            orden = OrdenVenta.objects.create(
                cliente=cliente,
                empleado=empleado,
                metodo_pago=metodo,
                estado_pago="pagado"
            )

            # 3. Agregar cada item como DetalleVenta
            for item in items:
                # Precio más reciente
                precio_actual = Precio.objects.filter(producto=item.producto).order_by('-fecha').first()
                if not precio_actual:
                    return Response({"error": f"No hay precio registrado para {item.producto.nombre}"}, status=400)

                subtotal = item.cantidad * precio_actual.valor

                DetalleVenta.objects.create(
                    orden=orden,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=precio_actual.valor,
                    subtotal=subtotal
                )

            # 4. Eliminar carrito (opcional)
            carrito.delete()

            return Response({
                "mensaje": "Pago confirmado",
                "orden_id": orden.id
            }, status=201)

        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=404)
        except Empleado.DoesNotExist:
            return Response({"error": "Empleado no encontrado"}, status=404)
        except Carrito.DoesNotExist:
            return Response({"error": "Carrito no encontrado"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)