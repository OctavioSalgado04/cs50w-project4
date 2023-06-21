function agregarAlCarrito() {
  var mensaje = document.createElement("div");
  mensaje.classList.add("alert", "alert-success");
  mensaje.textContent = "Agregado al carrito";

  var contenedorMensajes = document.getElementById("liveAlertPlaceholder");

  while (contenedorMensajes.firstChild) {
    contenedorMensajes.removeChild(contenedorMensajes.firstChild);
  }

  contenedorMensajes.appendChild(mensaje);
}


          

