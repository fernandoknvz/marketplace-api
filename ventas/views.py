from rest_framework import viewsets
from .models import Cliente, OrdenVenta, DetalleVenta
from .serializers import ClienteSerializer, OrdenVentaSerializer, DetalleVentaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenVentaCreateSerializer
from .models import OrdenVenta
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
