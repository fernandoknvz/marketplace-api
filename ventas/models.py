from django.db import models
from productos.models import Producto
from empleados.models import Empleado
from clientes.models import Cliente
class OrdenVenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ventas')  
    fecha = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, default='pendiente')
    
class DetalleVenta(models.Model):
    orden = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # desde tabla precios
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
