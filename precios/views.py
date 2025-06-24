from rest_framework import viewsets
from .models import Precio
from .serializers import PrecioSerializer

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializer
