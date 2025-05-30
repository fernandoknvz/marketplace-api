from django.contrib import admin
from .models import Cliente, OrdenVenta, DetalleVenta

admin.site.register(Cliente)
admin.site.register(OrdenVenta)
admin.site.register(DetalleVenta)
