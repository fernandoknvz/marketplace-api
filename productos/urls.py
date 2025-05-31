from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, detalle_producto

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')  # <--- aquí

urlpatterns = [
    path('', include(router.urls)),
    path('productos/<int:pk>/', detalle_producto, name='detalle-producto'),
]
