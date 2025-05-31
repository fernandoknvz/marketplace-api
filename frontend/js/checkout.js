document.getElementById("pagoForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const cliente_id = document.getElementById("cliente_id").value;
    const empleado_id = document.getElementById("empleado_id").value;
    const metodo = document.getElementById("metodo").value;

    // Mostrar el spinner y ocultar el formulario
    document.getElementById("spinner").style.display = "block";
    document.getElementById("pagoForm").style.display = "none";
    document.getElementById("mensaje").textContent = "";

    fetch("http://localhost:8000/api/confirmar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cliente_id: cliente_id,
            empleado_id: empleado_id,
            metodo_pago: metodo
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("spinner").style.display = "none";
        if (data.mensaje && data.orden_id) {
            document.getElementById("mensaje").textContent = "✅ Pago confirmado con éxito. Redirigiendo...";
            setTimeout(() => {
                window.location.href = `detalle.html?orden_id=${data.orden_id}`;
            }, 3000);
        } else if (data.error) {
            document.getElementById("pagoForm").style.display = "block";
            document.getElementById("mensaje").textContent = "❌ Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("spinner").style.display = "none";
        document.getElementById("pagoForm").style.display = "block";
        document.getElementById("mensaje").textContent = "❌ Error de conexión: " + error;
    });
});
