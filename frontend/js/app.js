const API_URL = 'http://localhost:8000/api/productos/';
const CATEGORIAS_URL = 'http://localhost:8000/api/categorias/';
const TASA_CAMBIO_URL = 'http://localhost:8000/api/ventas/tasa-cambio/';
const AGREGAR_URL = 'http://localhost:8000/api/carrito/agregar/';

async function cargarCategorias() {
  const res = await fetch(CATEGORIAS_URL);
  const data = await res.json();
  const select = document.getElementById("categoriaSelect");

  data.forEach(cat => {
    const opt = document.createElement("option");
    opt.value = cat.id;
    opt.textContent = cat.nombre;
    select.appendChild(opt);
  });
}

async function cargarProductos(categoriaId = "") {
  let url = API_URL;
  if (categoriaId) {
    url += `?categoria=${categoriaId}`;
  }

  const res = await fetch(url);
  const data = await res.json();
  const contenedor = document.getElementById('productos');

  contenedor.innerHTML = '';
  data.forEach(producto => {
    const div = document.createElement('div');
    div.className = 'card';

    div.innerHTML = `
      <img src="/static/img/${producto.id}.svg" alt="${producto.nombre}">
      <h3>${producto.nombre}</h3>
      <p><strong>Marca:</strong> ${producto.marca}</p>
      <p><strong>Precio:</strong> $${producto.precio_actual?.valor?.toLocaleString("es-CL") || 'No disponible'}</p>
      <button class="ver-detalle" data-id="${producto.id}">Ver Detalle</button>
    `;

    // Aseguramos que el botón funcione
    div.querySelector('.ver-detalle').addEventListener('click', (e) => {
      const id = e.target.dataset.id;
      verDetalle(id);
    });

    contenedor.appendChild(div);
  });
}


function filtrarPorCategoria() {
  const id = document.getElementById("categoriaSelect").value;
  cargarProductos(id);
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

  const modalContent = document.getElementById('detalle-modal-content');
  modalContent.innerHTML = `
  <div class="modal-grid">
    <div class="modal-img-container">
      <img src="/static/img/${data.id}.svg" alt="${data.nombre}" class="modal-img">
    </div>
    <div class="modal-info">
      <h2>${data.nombre}</h2>
      <p><strong>Marca:</strong> ${data.marca}</p>
      <p><strong>Stock:</strong> ${data.stock}</p>
      <p><strong>Precio:</strong> ${precioCLP} CLP</p>
      <p><strong>Precio en USD:</strong> $${precioUSD}</p>
      <p><strong>Fecha:</strong> ${data.precio_actual?.fecha || 'No disponible'}</p>
      <button id="btnAgregarCarrito">Agregar al Carrito</button>
    </div>
  </div>
`;



  document.getElementById("btnAgregarCarrito").addEventListener("click", () => {
    agregarAlCarrito(data.id);
  });

  document.getElementById("detalleModal").style.display = "flex";
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

function cerrarModal() {
  document.getElementById("detalleModal").style.display = "none";
}


// Inicializar
cargarCategorias();
cargarProductos();


async function convertirCLPaUSD() {
  const clp = parseFloat(document.getElementById("clpInput").value);
  const resultado = document.getElementById("resultadoUSD");

  if (isNaN(clp) || clp <= 0) {
    resultado.textContent = "Ingrese un valor válido.";
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/api/ventas/tasa-cambio/");
    const data = await res.json();
    const tasa = data?.usd_to_clp;

    if (!tasa || tasa <= 0) {
      resultado.textContent = "Tasa no disponible.";
      return;
    }

    const usd = (clp / tasa).toFixed(2);
    resultado.textContent = `USD $${usd}`;
  } catch (error) {
    console.error("Error consultando tasa:", error);
    resultado.textContent = "Error al convertir.";
  }
}


