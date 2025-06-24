from django.test import TestCase
from rest_framework.test import APIClient
from .models import OrdenVenta, DetalleVenta, Cliente
from empleados.models import Empleado
from productos.models import Producto, Categoria
from productos.models import Precio

class VentasTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()

        self.empleado = Empleado.objects.create(
            username='carlos',
            password='1234',
            rol='vendedor'
        )

        self.cliente = Cliente.objects.create(
            nombre='Luis',
            apellido='Alvarez',
            email='luis@example.com',
            password='abcd'
        )

        self.categoria = Categoria.objects.create(nombre='Electricidad')

        self.producto = Producto.objects.create(
            nombre='Bombilla LED',
            stock=100,
            categoria=self.categoria
        )

        self.orden = OrdenVenta.objects.create(
            cliente=self.cliente,
            empleado=self.empleado
        )

        self.detalle = DetalleVenta.objects.create(
            orden=self.orden,
            producto=self.producto,
            cantidad=2,
            precio_unitario=1990,
            subtotal=3980
        )

    def test_orden_venta_model(self):
        self.assertEqual(self.orden.estado_pago, 'pendiente')

    def test_detalle_venta_model(self):
        self.assertEqual(self.detalle.subtotal, 3980)

    def test_update_estado_pago(self):
        self.orden.estado_pago = 'pagado'
        self.orden.save()
        self.assertEqual(self.orden.estado_pago, 'pagado')

    def test_orden_detalle_relation(self):
        detalles = DetalleVenta.objects.filter(orden=self.orden)
        self.assertEqual(detalles.count(), 1)

    def test_create_orden_endpoint(self):
        response = self.client_api.post('/api/ordenes/', {
            'cliente': self.cliente.id,
            'empleado': self.empleado.id,
            'detalles': [
                {
                    'producto': self.producto.id,
                    'cantidad': 1,
                    'precio_unitario': 1990,
                    'subtotal': 1990
                }
            ]
        }, format='json')
        self.assertIn(response.status_code, [200, 201])

    def test_flujo_completo_crear_orden(self):
        response_cliente = self.client_api.post('/api/clientes/', {
            'nombre': 'Laura',
            'apellido': 'Gonzalez',
            'email': 'laura@example.com',
            'password': 'abc123'
        }, format='json')
        self.assertEqual(response_cliente.status_code, 201)
        cliente_id = response_cliente.data['id']

        response_orden = self.client_api.post('/api/ordenes/', {
            'cliente': cliente_id,
            'empleado': self.empleado.id,
            'detalles': [
                {
                    'producto': self.producto.id,
                    'cantidad': 2,
                    'precio_unitario': 1990,
                    'subtotal': 3980
                }
            ]
        }, format='json')
        self.assertIn(response_orden.status_code, [200, 201])
