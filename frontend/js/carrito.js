document.addEventListener("DOMContentLoaded", cargarCarrito);

const API_BASE = "http://localhost:8000/api";

function cargarCarrito() {
    fetch(`${API_BASE}/carrito/`)
        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById("carrito");
            contenedor.innerHTML = "";

            const btnPagar = document.querySelector("button[onclick*='checkout.html']");

            if (!data.items || data.items.length === 0) {
                contenedor.innerHTML = "<p>El carrito está vacío.</p>";
                if (btnPagar) {
                    btnPagar.disabled = true;
                    btnPagar.classList.add("disabled");
                }
                document.getElementById("total").textContent = "Total: $0";
                return;
            } else {
                if (btnPagar) {
                    btnPagar.disabled = false;
                    btnPagar.classList.remove("disabled");
                }
            }

            const formatter = new Intl.NumberFormat('es-CL');
            let html = "<table><thead><tr><th>Producto</th><th>Cantidad</th><th>Valor Unitario</th><th>Sub Total</th><th>Editar</th></tr></thead><tbody>";
            data.items.forEach((item, index) => {
                html += `
                <tr>
                    <td>${item.producto}</td>
                    <td><input type="number" min="1" value="${item.cantidad}" id="cantidad-${item.producto_id}"></td>
                    <td>$${formatter.format(item.valor_unitario)}</td>
                    <td>$${formatter.format(item.subtotal)}</td>
                    <td>
                      <button onclick="actualizarCantidad(${item.producto_id}, document.getElementById('cantidad-${item.producto_id}').value)">Actualizar</button>
                      <button onclick="eliminarItem(${item.producto_id})">Eliminar</button>
                    </td>
                </tr>`;
            });
            html += "</tbody></table>";

            contenedor.innerHTML = html;
            document.getElementById("total").textContent = `Total: $${formatter.format(data.total)}`;
        })
        .catch(error => console.error("Error al cargar el carrito:", error));
}


function vaciarCarrito() {
    fetch("http://localhost:8000/api/carrito/vaciar/", {
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
    fetch("http://localhost:8000/api/carrito/actualizar/", {
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

function eliminarItem(productoId) {
    if (confirm("¿Estás seguro de que deseas eliminar este producto del carrito?")) {
        fetch("http://localhost:8000/api/carrito/eliminar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ producto_id: productoId })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje || data.error);
            cargarCarrito(); // recarga el carrito
        })
        .catch(error => console.error("Error al eliminar el producto:", error));
    }
}


function mostrarModalCliente() {
    document.getElementById("clienteModal").style.display = "block";
}

document.getElementById("btnRegistrar").addEventListener("click", function () {
    document.getElementById("clienteModal").style.display = "none";
    // Redirigir a pantalla de login/registro
    window.location.href = "registro.html"; // o login.html si lo separas
});

document.getElementById("btnInvitado").addEventListener("click", function () {
    document.getElementById("clienteModal").style.display = "none";
    // Continuar al checkout como invitado
    window.location.href = "checkout.html?invitado=true";
});