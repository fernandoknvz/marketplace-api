from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, CategoriaViewSet, detalle_producto  # ⬅️ importa el viewset

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'categorias', CategoriaViewSet, basename='categorias')  # ⬅️ agrega esta línea

urlpatterns = [
    path('', include(router.urls)),
    path('productos/<int:pk>/', detalle_producto, name='detalle-producto'),
]
