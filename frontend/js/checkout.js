document.getElementById("pagoForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const cliente_id = document.getElementById("cliente_id").value;
    const empleado_id = 1;  // ID real de "VENTA ONLINE"
    const metodo = document.getElementById("metodo").value;
    const titular = document.getElementById("titular").value.trim();
    const tarjeta = document.getElementById("tarjeta").value.trim().replace(/\s+/g, '');
    const vencimiento = document.getElementById("vencimiento").value.trim();
    const cvv = document.getElementById("cvv").value.trim();
    const mensaje = document.getElementById("mensaje");

    document.getElementById("spinner").style.display = "block";
    document.getElementById("pagoForm").style.display = "none";
    mensaje.textContent = "";

    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(titular)) {
        mostrarError("❌ El nombre del titular solo puede contener letras y espacios.");
        return;
    }

    if (!/^\d{13,19}$/.test(tarjeta)) {
        mostrarError("❌ El número de tarjeta debe contener 16 dígitos.");
        return;
    }

    if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(vencimiento)) {
        mostrarError("❌ Fecha ingresada no válida (ejemplo: 08/26).");
        return;
    }

    const [mes, anio] = vencimiento.split('/');
    const mesNum = parseInt(mes);
    const anioNum = parseInt(anio);
    const fechaActual = new Date();
    const mesActual = fechaActual.getMonth() + 1;
    const anioActual = fechaActual.getFullYear() % 100;

    if (anioNum < anioActual || (anioNum === anioActual && mesNum < mesActual)) {
        mostrarError("❌ La tarjeta está vencida.");
        return;
    }

    if (!/^\d{3}$/.test(cvv)) {
        mostrarError("❌ El CVV debe contener exactamente 3 dígitos.");
        return;
    }

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
            mensaje.textContent = "✅ Pago confirmado con éxito. Redirigiendo...";
            setTimeout(() => {
                window.location.href = `detalle.html?orden_id=${data.orden_id}`;
            }, 3000);
        } else {
            mostrarError("❌ Error: " + (data.error || "Error inesperado"));
        }
    })
    .catch(error => {
        mostrarError("❌ Error de conexión: " + error);
    });

    function mostrarError(texto) {
        mensaje.textContent = texto;
        document.getElementById("spinner").style.display = "none";
        document.getElementById("pagoForm").style.display = "block";
    }
});

document.getElementById("tarjeta").addEventListener("input", function () {
    let valor = this.value.replace(/\D/g, '').slice(0, 19);
    this.value = valor.replace(/(.{4})/g, '$1 ').trim();
});

document.getElementById("vencimiento").addEventListener("input", function () {
    let valor = this.value.replace(/[^\d]/g, '');
    if (valor.length >= 3) {
        this.value = valor.slice(0, 2) + '/' + valor.slice(2, 4);
    } else {
        this.value = valor;
    }
});

document.getElementById("cvv").addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, '').slice(0, 3);
});

document.getElementById("titular").addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
});
