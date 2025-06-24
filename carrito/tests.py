from django.test import TestCase
from rest_framework.test import APIClient
from .models import Carrito, ItemCarrito
from productos.models import Producto, Categoria

class CarritoModelTest(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.categoria = Categoria.objects.create(nombre='Ferretería')
        self.producto = Producto.objects.create(
            nombre='Martillo',
            stock=50,
            categoria=self.categoria
        )
        self.carrito = Carrito.objects.create()

    def test_crear_carrito(self):
        self.assertIsNotNone(self.carrito.id)

    def test_add_itemcarrito_model(self):
        item = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=3)
        self.assertEqual(item.cantidad, 3)

    def test_get_carrito_endpoint(self):
        response = self.client_api.get('/api/carrito/')
        self.assertEqual(response.status_code, 200)

    def test_add_to_carrito_endpoint(self):
        response = self.client_api.post('/api/carrito/agregar/', {
            'producto_id': self.producto.id,
            'cantidad': 2
        }, format='json')
        self.assertIn(response.status_code, [200, 201])

    def test_invalid_producto_add_to_carrito(self):
        response = self.client_api.post('/api/carrito/agregar/', {
            'producto_id': 9999,
            'cantidad': 1
        }, format='json')
        self.assertEqual(response.status_code, 404)

    def test_add_multiple_items_to_carrito(self):
        producto2 = Producto.objects.create(
            nombre='Destornillador',
            stock=30,
            categoria=self.categoria
        )
        response1 = self.client_api.post('/api/carrito/agregar/', {
            'producto_id': self.producto.id,
            'cantidad': 1
        }, format='json')
        response2 = self.client_api.post('/api/carrito/agregar/', {
            'producto_id': producto2.id,
            'cantidad': 2
        }, format='json')
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)

