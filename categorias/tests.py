from django.test import TestCase
from rest_framework.test import APIClient
from .models import Categoria
from django.urls import reverse

class CategoriaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre='Ferretería')

    def test_crear_categoria(self):
        response = self.client.post('/api/categorias/', {'nombre': 'Jardinería'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Categoria.objects.filter(nombre='Jardinería').count(), 1)

    def test_obtener_lista_categorias(self):
        response = self.client.get('/api/categorias/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtener_detalle_categoria(self):
        response = self.client.get(f'/api/categorias/{self.categoria.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'Ferretería')

    def test_actualizar_categoria(self):
        response = self.client.put(
            f'/api/categorias/{self.categoria.id}/',
            {'nombre': 'Construcción'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Construcción')

    def test_eliminar_categoria(self):
        response = self.client.delete(f'/api/categorias/{self.categoria.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())

    def test_crear_categoria_nombre_vacio(self):
        response = self.client.post('/api/categorias/', {'nombre': ''})
        self.assertEqual(response.status_code, 400)
