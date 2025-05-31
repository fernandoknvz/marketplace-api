const API_URL = 'http://localhost:8000/api/productos/';
const TASA_CAMBIO_URL = 'http://localhost:8000/api/ventas/tasa-cambio/';
const AGREGAR_URL = 'http://localhost:8000/api/agregar/';

async function cargarProductos() {
  const res = await fetch(API_URL);
  const data = await res.json();
  const contenedor = document.getElementById('productos');

  contenedor.innerHTML = '';
  data.forEach(producto => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <h3>${producto.nombre}</h3>
      <p><strong>Marca:</strong> ${producto.marca}</p>
      <p><strong>Stock:</strong> ${producto.stock}</p>
      <button onclick="verDetalle(${producto.id})">Ver Detalle</button>
    `;
    contenedor.appendChild(div);
  });
}

async function verDetalle(id) {
  const resProducto = await fetch(API_URL + id + '/');
  const data = await resProducto.json();

  let precioCLP = data.precio_actual?.valor || 0;
  let precioUSD = 'No disponible';

  try {
    const resTasa = await fetch(TASA_CAMBIO_URL);
    const tasa = await resTasa.json();
    if (precioCLP > 0 && tasa.usd_to_clp > 0) {
      precioUSD = (precioCLP / tasa.usd_to_clp).toFixed(2);
    }
  } catch (error) {
    console.error("Error obteniendo la tasa de cambio:", error);
  }

  const detalle = document.getElementById('detalle');
  detalle.innerHTML = `
    <h2>${data.nombre}</h2>
    <p><strong>Marca:</strong> ${data.marca}</p>
    <p><strong>Stock:</strong> ${data.stock}</p>
    <p><strong>Precio:</strong> ${precioCLP} CLP</p>
    <p><strong>Precio en USD:</strong> $${precioUSD}</p>
    <p><strong>Fecha:</strong> ${data.precio_actual?.fecha || 'No disponible'}</p>
    <button onclick="agregarAlCarrito(${data.id})">Agregar al Carrito</button>
  `;
}

async function agregarAlCarrito(idProducto) {
  const res = await fetch(AGREGAR_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      producto_id: idProducto,
      cantidad: 1
    })
  });

  const data = await res.json();
  if (res.ok) {
    alert("Producto agregado al carrito correctamente.");
  } else {
    alert("Error al agregar al carrito: " + (data?.error || JSON.stringify(data)));
  }
}

cargarProductos();
