function validarTarjeta() {
  var nombreTarjeta = document.getElementById("nombre-tarjeta").value;
  var numeroTarjeta = document.getElementById("numero-tarjeta").value;
  var fechaExpiracion = document.getElementById("fecha-expiracion").value;
  var cvv = document.getElementById("cvv").value;
  
  var regexSoloLetras = /^[a-zA-Z\s]+$/;
  var regexNumeroTarjeta = /^\d{16}$/;
  var regexFechaExpiracion = /^\d{2}\/\d{2}$/;
  var regexCVV = /^\d{3}$/;
  
  if (!regexSoloLetras.test(nombreTarjeta)) {
    alert("El nombre en la tarjeta solo puede contener letras y espacios.");
    return false;
  }
  
  if (!regexNumeroTarjeta.test(numeroTarjeta)) {
    alert("El número de tarjeta debe tener 16 dígitos.");
    return false;
  }
  
  if (!regexFechaExpiracion.test(fechaExpiracion)) {
    alert("La fecha de expiración debe tener el formato MM/AA.");
    return false;
  }
  
  if (!regexCVV.test(cvv)) {
    alert("El CVV debe tener 3 dígitos.");
    return false;
  }
  
  return true;
}