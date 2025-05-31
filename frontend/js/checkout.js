document.getElementById("pagoForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const cliente_id = document.getElementById("cliente_id").value;
    const empleado_id = document.getElementById("empleado_id").value;
    const metodo = document.getElementById("metodo").value;

    fetch("http://localhost:8000/api/confirmar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cliente_id: cliente_id,
            empleado_id: empleado_id,
            metodo_pago: metodo  // opcional, simbólico
        })
    })
    .then(response => response.json())
    .then(data => {
        const mensaje = document.getElementById("mensaje");
        if (data.mensaje) {
            mensaje.innerHTML = `<strong>${data.mensaje}</strong><br>
                Orden ID: ${data.orden_id}<br>
                Total: $${data.total}`;
        } else if (data.error) {
            mensaje.textContent = "Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("mensaje").textContent = "Error de conexión: " + error;
    });
});
