from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('carrito.urls')),
    path('api/', include('categorias.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('empleados.urls')),
    path('api/', include('precios.urls')),
    path('api/', include('productos.urls')),
    path('api/', include('proveedores.urls')),
    path('api/', include('ventas.urls')),
]
