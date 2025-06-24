# productos/tests.py

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from categorias.models import Categoria
from productos.models import Producto

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def categoria_test():
    return Categoria.objects.create(
        nombre="Categoria Test",
        descripcion="Descripción de categoría test"
    )

@pytest.fixture
def producto_test(categoria_test):
    return Producto.objects.create(
        codigo_producto="TEST001",
        nombre="Producto Test",
        marca="Marca Test",
        stock=10,
        categoria=categoria_test,
        imagen_url="https://example.com/imagen.jpg"
    )

@pytest.mark.django_db
def test_listar_productos(api_client, producto_test):
    url = reverse('producto-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_detalle_producto(api_client, producto_test):
    url = reverse('producto-detail', args=[producto_test.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['nombre'] == producto_test.nombre

@pytest.mark.django_db
def test_crear_producto(api_client, categoria_test):
    url = reverse('producto-list')
    data = {
        "codigo_producto": "TEST002",
        "nombre": "Producto Nuevo",
        "marca": "Marca Nueva",
        "stock": 5,
        "categoria": categoria_test.id,
        "imagen_url": "https://example.com/nueva.jpg"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Producto.objects.filter(nombre="Producto Nuevo").exists()

@pytest.mark.django_db
def test_actualizar_producto(api_client, producto_test):
    url = reverse('producto-detail', args=[producto_test.id])
    updated_data = {
        "codigo_producto": producto_test.codigo_producto,
        "nombre": "Producto Actualizado",
        "marca": producto_test.marca,
        "stock": producto_test.stock + 5,
        "categoria": producto_test.categoria.id,
        "imagen_url": producto_test.imagen_url
    }
    response = api_client.put(url, updated_data, format='json')
    assert response.status_code == 200
    producto_test.refresh_from_db()
    assert producto_test.nombre == "Producto Actualizado"

@pytest.mark.django_db
def test_eliminar_producto(api_client, producto_test):
    url = reverse('producto-detail', args=[producto_test.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Producto.objects.filter(id=producto_test.id).exists()

@pytest.mark.django_db
def test_listar_productos_vacio(api_client):
    url = reverse('producto-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0
