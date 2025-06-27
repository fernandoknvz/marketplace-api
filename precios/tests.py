from django.test import TestCase
from rest_framework.test import APIClient
from .models import Precio
from productos.models import Producto
from datetime import date
from decimal import Decimal

class PrecioAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producto = Producto.objects.create(nombre='Martillo', stock=100)
        self.precio = Precio.objects.create(producto=self.producto, valor=5000, fecha=date.today())

    def test_crear_precio(self):
        response = self.client.post('/api/precios/', {
            'producto': self.producto.id,
            'valor': 6000,
            'fecha': '2024-06-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Precio.objects.filter(valor=6000).count(), 1)

    def test_obtener_lista_precios(self):
        response = self.client.get('/api/precios/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtener_detalle_precio(self):
        response = self.client.get(f'/api/precios/{self.precio.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.data['valor']), self.precio.valor)

    def test_actualizar_precio(self):
        response = self.client.put(
            f'/api/precios/{self.precio.id}/',
            {
                'producto': self.producto.id,
                'valor': 7000,
                'fecha': str(date.today())
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.precio.refresh_from_db()
        self.assertEqual(self.precio.valor, 7000)

    def test_eliminar_precio(self):
        response = self.client.delete(f'/api/precios/{self.precio.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Precio.objects.filter(id=self.precio.id).exists())

    def test_crear_precio_valor_vacio(self):
        response = self.client.post('/api/precios/', {
            'producto': self.producto.id,
            'valor': '',
            'fecha': '2024-06-01'
        })
        self.assertEqual(response.status_code, 400)
