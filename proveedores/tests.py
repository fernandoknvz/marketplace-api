from django.test import TestCase
from rest_framework.test import APIClient
from .models import Proveedor

class ProveedorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.proveedor = Proveedor.objects.create(
            nombre='Proveedor Test',
            rut='12.345.678-9',
            direccion='Calle Falsa 123',
            telefono='912345678',
            email='proveedor@test.com'
        )

    def test_crear_proveedor(self):
        response = self.client.post('/api/proveedores/', {
            'nombre': 'Proveedora ABC',
            'rut': '98.765.432-1',
            'direccion': 'Nueva Calle 456',
            'telefono': '987654321',
            'email': 'abc@correo.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Proveedor.objects.filter(nombre='Proveedora ABC').count(), 1)

    def test_obtener_lista_proveedores(self):
        response = self.client.get('/api/proveedores/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtener_detalle_proveedor(self):
        response = self.client.get(f'/api/proveedores/{self.proveedor.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'Proveedor Test')

    def test_actualizar_proveedor(self):
        response = self.client.put(
            f'/api/proveedores/{self.proveedor.id}/',
            {
                'nombre': 'Proveedor Actualizado',
                'rut': '98.765.432-1',
                'direccion': 'Nueva Calle 456',
                'telefono': '987654321',
                'email': 'nuevo@correo.com'
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.proveedor.refresh_from_db()
        self.assertEqual(self.proveedor.nombre, 'Proveedor Actualizado')

    def test_eliminar_proveedor(self):
        response = self.client.delete(f'/api/proveedores/{self.proveedor.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Proveedor.objects.filter(id=self.proveedor.id).exists())

    def test_crear_proveedor_campos_vacios(self):
        response = self.client.post('/api/proveedores/', {
            'nombre': '',
            'rut': '',
            'email': ''
        })
        self.assertEqual(response.status_code, 400)
