from django.urls import path
from .views import CarritoListAPIView, AgregarItemCarritoAPIView

urlpatterns = [
    path('carrito/', CarritoListAPIView.as_view(), name='carrito-list'),
    path('carrito/agregar/', AgregarItemCarritoAPIView.as_view(), name='carrito-add'),
]
