// frontend/app.js
const API_URL = "http://localhost:8000/api/productos/";

function cargarProductos() {
    const categoria = document.getElementById("categoria").value;
    const url = `${API_URL}?categoria=${categoria}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById("resultado");
            contenedor.innerHTML = "<h2>Resultados:</h2>";

            if (data.length === 0) {
                contenedor.innerHTML += "<p>No se encontraron productos.</p>";
                return;
            }

            let lista = "<ul>";
            data.forEach(prod => {
                lista += `<li><strong>${prod.nombre}</strong> - ${prod.marca} - Stock: ${prod.stock}</li>`;
            });
            lista += "</ul>";

            contenedor.innerHTML += lista;
        })
        .catch(error => {
            console.error("Error al obtener productos:", error);
        });
}
