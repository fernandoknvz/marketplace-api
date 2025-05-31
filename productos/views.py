from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria_id = self.request.query_params.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset


@api_view(['GET'])
def detalle_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto)
    return Response(serializer.data)