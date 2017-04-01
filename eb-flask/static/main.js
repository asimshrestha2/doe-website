window.onload = function() {
  var inputHTML = document.getElementsByTagName('input');
  for (var i = 0; i < inputHTML.length; i++) {
    if(inputHTML[i].type == "text" || inputHTML[i].type == "password"){
      this.addEventListener("keyup", function(e){
        inputE = e.srcElement;
        inputE.setAttribute('value', inputE.value);
      });
    }
  }
}
