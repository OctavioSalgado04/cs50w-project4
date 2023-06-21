function select(value) {
  var baseUrl = window.location.href.split('/'); // Obtiene la URL base actual
  baseUrl.pop(); // Elimina la última parte de la URL (nombre del archivo actual)
  var newUrl = baseUrl.join('/') + value; // Concatena la URL base con el valor seleccionado
  window.location.href = newUrl; // Redirige a la nueva URL
}
