from django.urls import path
from .views import CarritoListAPIView, AgregarItemCarritoAPIView, VaciarCarritoAPIView, ActualizarItemCarritoAPIView, EliminarItemCarritoAPIView

urlpatterns = [
    path('carrito/', CarritoListAPIView.as_view(), name='carrito-list'),
    path('carrito/agregar/', AgregarItemCarritoAPIView.as_view(), name='carrito-add'),
    path('carrito/vaciar/', VaciarCarritoAPIView.as_view(), name='carrito-vaciar'),
    path('carrito/actualizar/', ActualizarItemCarritoAPIView.as_view(), name='carrito-actualizar'),
     path('carrito/eliminar/', EliminarItemCarritoAPIView.as_view()),

]
