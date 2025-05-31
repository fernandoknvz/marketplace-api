from django.db import models
from productos.models import Producto
from empleados.models import Empleado


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  

    class Meta:
        db_table = 'cliente'
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class OrdenVenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ventas')  
    fecha = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, default='pendiente')
    class Meta:
        db_table = 'orden_venta'  

    def __str__(self):
        return f"Orden #{self.id} - Cliente: {self.cliente.nombre} {self.cliente.apellido}"
   
    
class DetalleVenta(models.Model):
    orden = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # desde tabla precios
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_venta'
        managed = False

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"    