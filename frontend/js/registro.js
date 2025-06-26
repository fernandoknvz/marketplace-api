document.getElementById("formRegistro").addEventListener("submit", function (e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const mensaje = document.getElementById("mensaje");

  fetch("http://localhost:8000/api/registro/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      nombre,
      apellido,
      email,
      password
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.id || data.success) {
      mensaje.textContent = "✅ Registro exitoso. Redirigiendo al pago...";
      setTimeout(() => {
        window.location.href = `checkout.html?cliente_id=${data.id || data.cliente_id}`;
      }, 3000);
    } else {
      mensaje.textContent = "❌ Error: " + (data.error || "Revisa los datos ingresados.");
    }
  })
  .catch(error => {
    mensaje.textContent = "❌ Error de conexión: " + error;
  });
});
