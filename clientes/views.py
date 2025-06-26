from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConsultaContactoSerializer, ClienteSerializer

class RegistroClienteView(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            return Response({
                "mensaje": "Cliente registrado exitosamente",
                "id": cliente.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultaContactoAPIView(APIView):
    def post(self, request):
        serializer = ConsultaContactoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Consulta enviada exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
