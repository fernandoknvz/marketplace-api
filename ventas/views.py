from rest_framework import viewsets
from .models import Cliente, OrdenVenta, DetalleVenta
from .serializers import ClienteSerializer, OrdenVentaSerializer, DetalleVentaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenVentaCreateSerializer

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