window.onload = function() {
  var inputHTML = document.getElementsByTagName('input');
  for (var i = 0; i < inputHTML.length; i++) {
    if(inputHTML[i].type == "text" || inputHTML[i].type == "password"){
      this.addEventListener("keyup", function(e){
        inputE = e.srcElement || e.target;
        inputE.setAttribute('value', inputE.value);
      });
    }
  }

  var menubtn = document.getElementById('menubtn');
  if (menubtn) {
    menubtn.addEventListener('click', function(e) {
      document.getElementById('menu-content').classList.toggle("show");
    });
  }
}
