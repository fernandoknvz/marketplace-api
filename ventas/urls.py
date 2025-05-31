from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, OrdenVentaViewSet, DetalleVentaViewSet
from django.urls import path, include
from .views import RegistrarVentaAPIView, SimularPagoView, TasaCambioView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'ordenes', OrdenVentaViewSet)
router.register(r'detalles', DetalleVentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ventas/registrar/', RegistrarVentaAPIView.as_view(), name='registrar-venta'),
    path('ventas/<int:pk>/pagar/', SimularPagoView.as_view(), name='simular-pago'),
    path('ventas/tasa-cambio/', TasaCambioView.as_view(), name='tasa-cambio'),
]
