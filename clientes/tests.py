from django.test import TestCase
from rest_framework.test import APIClient
from .models import Cliente, ConsultaContacto

class ClienteTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()

    def test_cliente_model(self):
        cliente = Cliente.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan@example.com',
            password='123456'
        )
        self.assertEqual(cliente.email, 'juan@example.com')

    def test_duplicate_email_cliente(self):
        Cliente.objects.create(nombre='Juan', apellido='Pérez', email='test@example.com', password='123')
        with self.assertRaises(Exception):
            Cliente.objects.create(nombre='Otro', apellido='Cliente', email='test@example.com', password='456')

    def test_cliente_str(self):
        cliente = Cliente.objects.create(nombre='Sofia', apellido='Martinez', email='sofia@example.com', password='123')
        self.assertEqual(str(cliente), 'Sofia Martinez')

    def test_create_cliente_endpoint(self):
        response = self.client_api.post('/api/clientes/', {
            'nombre': 'Ana',
            'apellido': 'Gómez',
            'email': 'ana@example.com',
            'password': 'abcdef'
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_consulta_contacto_model(self):
        consulta = ConsultaContacto.objects.create(
            nombre='Pedro',
            correo='pedro@example.com',
            mensaje='Consulta prueba'
        )
        self.assertEqual(consulta.nombre, 'Pedro')

    def test_contacto_endpoint(self):
        response = self.client_api.post('/api/contacto/', {
            'nombre': 'Pedro',
            'correo': 'pedro@example.com',
            'mensaje': 'Consulta de prueba'
        }, format='json')
        self.assertEqual(response.status_code, 201)
