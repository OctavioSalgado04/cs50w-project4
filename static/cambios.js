function enviarURLFoto(urlFoto) {
    fetch('/guardar_cambios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ urlFoto: urlFoto })
    })
    .then(function(response) {
        // Manejar la respuesta del servidor
        if (response.ok) {
          // Redirigir a la página principal
          window.location.href = "/";
        }
      })
      .catch(function(error) {
        // Manejar errores de la solicitud
      });
}
var cambiosRealizados = false;
function mostrarCampo(campo) {
  if (campo === 'nombre') {
    document.getElementById('valorNombre').style.display = 'none';
    document.getElementById('btnNombre').style.display = 'none';
    document.getElementById('campoNombre').style.display = 'block';
    document.getElementById('campoNombre').querySelector('input').value = '';
  } else if (campo === 'correo') {
    document.getElementById('valorCorreo').style.display = 'none';
    document.getElementById('btnCorreo').style.display = 'none';
    document.getElementById('campoCorreo').style.display = 'block';
    document.getElementById('campoCorreo').querySelector('input').value = '';
  } else if (campo === 'direccion') {
    document.getElementById('valorDireccion').style.display = 'none';
    document.getElementById('btnDireccion').style.display = 'none';
    document.getElementById('campoDireccion').style.display = 'block';
    document.getElementById('campoDireccion').querySelector('input').value = '';
  } else if (campo === 'descripcion') {
    document.getElementById('valorDescripcion').style.display = 'none';
    document.getElementById('btnDescripcion').style.display = 'none';
    document.getElementById('campoDescripcion').style.display = 'block';
    document.getElementById('campoDescripcion').querySelector('input').value = '';
  }
} 

function cambiarDato(campo) {
  if (campo === 'nombre') {
    var nuevoNombre = document.getElementById('nuevoNombre').value;
    document.getElementById('valorNombre').innerText = nuevoNombre;
    document.getElementById('valorNombre').style.display = 'block';
    document.getElementById('btnNombre').style.display = 'block';
    document.getElementById('campoNombre').style.display = 'none';
  } else if (campo === 'correo') {
    var nuevoCorreo = document.getElementById('nuevoCorreo').value;
    document.getElementById('valorCorreo').innerText = nuevoCorreo;
    document.getElementById('valorCorreo').style.display = 'block';
    document.getElementById('btnCorreo').style.display = 'block';
    document.getElementById('campoCorreo').style.display = 'none';
  } else if (campo === 'direccion') {
    var nuevoCorreo = document.getElementById('nuevoDireccion').value;
    document.getElementById('valorDireccion').innerText = nuevoDireccion;
    document.getElementById('valorDireccion').style.display = 'block';
    document.getElementById('btnDireccion').style.display = 'block';
    document.getElementById('campoDireccion').style.display = 'none';
  } else if (campo === 'descripcion') {
    var nuevoCorreo = document.getElementById('nuevoDireccion').value;
    document.getElementById('valorDescripcion').innerText = nuevoDireccion;
    document.getElementById('valorDescripcion').style.display = 'block';
    document.getElementById('btnDescripcion').style.display = 'block';
    document.getElementById('campoDescripcion').style.display = 'none';
  }
  cambiosRealizados = true; // Se han realizado cambios
  mostrarBotonGuardarCambios();
} 

function mostrarBotonGuardarCambios() {
  var btnGuardarCambios = document.getElementById('btnGuardarCambios');
  if (cambiosRealizados) {
    btnGuardarCambios.style.display = 'block';
  } else {
    btnGuardarCambios.style.display = 'none';
  }
}

function guardarCambios() {
  // Obtener los valores actualizados de los campos
  var nuevoNombre = document.getElementById('nuevoNombre').value;
  var nuevoCorreo = document.getElementById('nuevoCorreo').value;
  var nuevoDireccion = document.getElementById('nuevoDireccion').value;
  var nuevoDescripcion = document.getElementById('nuevoDescripcion').value;

  // Crear un objeto con los datos actualizados
  var datosActualizados = {
    nombre: nuevoNombre,
    correo: nuevoCorreo,
    direccion: nuevoDireccion,
    descripcion: nuevoDescripcion
  };

  // Hacer una solicitud POST a app.py con los datos actualizados
  fetch('/guardar_cambios', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(datosActualizados)
  })
  .then(function(response) {
    // Manejar la respuesta del servidor
    if (response.ok) {
      // Redirigir a la página principal
      window.location.href = "/";
    }
  })
  .catch(function(error) {
    // Manejar errores de la solicitud
  });
}
