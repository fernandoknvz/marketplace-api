from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CarritoViewSet, AgregarAlCarritoView, VerCarritoView, ConfirmarCompraView

router = DefaultRouter()
router.register(r'carrito', CarritoViewSet)

urlpatterns = router.urls + [
    path('agregar/', AgregarAlCarritoView.as_view(), name='carrito-agregar'),
    path('ver/', VerCarritoView.as_view(), name='carrito-ver'),
    path('confirmar/', ConfirmarCompraView.as_view(), name='confirmar-compra'),
]

