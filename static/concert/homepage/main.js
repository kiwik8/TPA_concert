setInterval(function () {
    const show = document.querySelector('span[data-show]')
    const next = show.nextElementSibling || document.querySelector('span:first-child')
    const up = document.querySelector('span[data-up]')
    
    if (up) {
      up.removeAttribute('data-up')
    }
    
    show.removeAttribute('data-show')
    show.setAttribute('data-up', '')
    
    next.setAttribute('data-show', '')
  }, 2000)

function checkRedirectCookie() {
  // Récupération des cookies sous forme de chaîne
  var cookies = document.cookie;
  // Séparation des cookies en tableau
  var cookiesArray = cookies.split("; ");
  // Boucle pour vérifier chaque cookie
  for (var i = 0; i < cookiesArray.length; i++) {
    // Séparation de la clé et de la valeur
    var keyValue = cookiesArray[i].split("=");
    // Vérification si la clé est "redirect" et la valeur est "true"
    if (keyValue[0] == "redirected" && keyValue[1] == "true") {
      return true;
    }
  }
  return false;
}
  

document.addEventListener('keydown', function(event) {
  document.location.href = "/home";
});
document.addEventListener('click', function(event) {
  document.location.href = "/home";
});