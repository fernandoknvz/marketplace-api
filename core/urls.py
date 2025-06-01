from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('productos.urls')),
    path('api/', include('carrito.urls')),
    path('api/', include('ventas.urls')),
    path('api/', include('clientes.urls')),
]
