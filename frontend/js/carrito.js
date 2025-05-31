document.addEventListener("DOMContentLoaded", cargarCarrito);

function cargarCarrito() {
    fetch("http://localhost:8000/api/ver/")
        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById("carrito");
            contenedor.innerHTML = "";

            if (data.carrito.length === 0) {
                contenedor.innerHTML = "<p>El carrito está vacío.</p>";
                return;
            }

            let html = "<table><thead><tr><th>Producto</th><th>Cantidad</th><th>Precio Unitario</th><th>Subtotal</th><th>Actualizar</th></tr></thead><tbody>";
            data.carrito.forEach((item, index) => {
                html += `<tr>
                    <td>${item.producto}</td>
                    <td>
                        <input type="number" min="1" value="${item.cantidad}" id="cantidad-${index}">
                    </td>
                    <td>$${item.precio_unitario}</td>
                    <td>$${item.subtotal}</td>
                    <td>
                        <button onclick="actualizarCantidad(${item.producto_id}, document.getElementById('cantidad-${index}').value)">Actualizar</button>
                    </td>
                </tr>`;
            });
            html += "</tbody></table>";

            contenedor.innerHTML = html;
            document.getElementById("total").textContent = "Total: $" + data.total;
        })
        .catch(error => console.error("Error al cargar el carrito:", error));
}

function vaciarCarrito() {
    fetch("http://localhost:8000/api/ventas/vaciar-carrito/", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje);
        cargarCarrito();
    })
    .catch(error => console.error("Error al vaciar el carrito:", error));
}

function actualizarCantidad(productoId, nuevaCantidad) {
    fetch("http://localhost:8000/api/agregar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            producto_id: productoId,
            cantidad: parseInt(nuevaCantidad)
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Cantidad actualizada");
        cargarCarrito();
    })
    .catch(error => console.error("Error al actualizar cantidad:", error));
}
