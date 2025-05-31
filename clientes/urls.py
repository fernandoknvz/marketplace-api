from django.urls import path
from .views import RegistroClienteView, ConsultaContactoAPIView

urlpatterns = [
    path('registro/', RegistroClienteView.as_view(), name='registro-cliente'),
    path('contacto/', ConsultaContactoAPIView.as_view(), name='consulta-contacto'),
]
