from django.test import TestCase
from rest_framework.test import APIClient
from .models import Empleado

class EmpleadoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.empleado = Empleado.objects.create(
            username='juanperez',
            password='123456',
            email='juan@ejemplo.com',
            rol='vendedor'
        )

    def test_crear_empleado(self):
        response = self.client.post('/api/empleados/', {
            'username': 'anagonzalez',
            'password': '654321',
            'email': 'ana@ejemplo.com',
            'rol': 'vendedor'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Empleado.objects.filter(username='anagonzalez').count(), 1)

    def test_obtener_lista_empleados(self):
        response = self.client.get('/api/empleados/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtener_detalle_empleado(self):
        response = self.client.get(f'/api/empleados/{self.empleado.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'juanperez')

    def test_actualizar_empleado(self):
        response = self.client.put(
            f'/api/empleados/{self.empleado.id}/',
            {
                'username': 'juan_actualizado',
                'password': '123456',
                'email': 'juan@ejemplo.com',
                'rol': 'vendedor',
                'activo': True
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.username, 'juan_actualizado')

    def test_eliminar_empleado(self):
        response = self.client.delete(f'/api/empleados/{self.empleado.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Empleado.objects.filter(id=self.empleado.id).exists())

    def test_crear_empleado_campos_vacios(self):
        response = self.client.post('/api/empleados/', {
            'username': '',
            'password': '',
            'rol': ''
        })
        self.assertEqual(response.status_code, 400)
