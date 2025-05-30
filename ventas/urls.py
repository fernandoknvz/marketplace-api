from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, OrdenVentaViewSet, DetalleVentaViewSet
from django.urls import path, include
from .views import RegistrarVentaAPIView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'ordenes', OrdenVentaViewSet)
router.register(r'detalles', DetalleVentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ventas/registrar/', RegistrarVentaAPIView.as_view(), name='registrar-venta'),
]
