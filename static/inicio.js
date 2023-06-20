const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

function select(value) {
  var baseUrl = window.location.href.split('/'); // Obtiene la URL base actual
  baseUrl.pop(); // Elimina la última parte de la URL (nombre del archivo actual)
  var newUrl = baseUrl.join('/') + value; // Concatena la URL base con el valor seleccionado
  window.location.href = newUrl; // Redirige a la nueva URL
}
