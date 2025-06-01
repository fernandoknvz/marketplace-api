document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const ordenId = params.get("orden_id");
  const contenedor = document.getElementById("detalle-compra");

  if (!ordenId) {
    contenedor.innerHTML = "<p>No se encontró una orden válida.</p>";
    return;
  }

  fetch(`http://localhost:8000/api/orden/${ordenId}/`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        contenedor.innerHTML = "<p>Error: " + data.error + "</p>";
        return;
      }

      const formatter = new Intl.NumberFormat('es-CL');

      let html = `<h2>Orden de Compra #${ordenId}</h2>`;
      html += `
        <table>
          <thead>
            <tr>
              <th>Producto</th>
              <th>Cantidad</th>
              <th>Precio Unitario</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
      `;

      data.detalle.forEach(item => {
        html += `
          <tr>
            <td>${item.producto}</td>
            <td>${item.cantidad}</td>
            <td>$${formatter.format(item.precio_unitario)}</td>
            <td>$${formatter.format(item.subtotal)}</td>
          </tr>
        `;
      });

      html += `
          </tbody>
        </table>
        <p style="text-align: right; margin-top: 1em;"><strong>Total pagado:</strong> $${formatter.format(data.total)}</p>
      `;

      contenedor.innerHTML = html;

      document.getElementById("mensaje-final").innerHTML = `
        ✅ Gracias por su compra. Será redirigido al inicio en 5 segundos...
      `;

      setTimeout(() => {
        window.location.href = "index.html";
      }, 5000);
    })
    .catch(err => {
      contenedor.innerHTML = "<p>Error de conexión: " + err + "</p>";
    });
});
