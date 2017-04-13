window.onload = function() {
  var inputHTML = document.getElementsByTagName('input');
  for (var i = 0; i < inputHTML.length; i++) {
    if(inputHTML[i].type == "text" || inputHTML[i].type == "password"){
      this.addEventListener("input", function(e){
        inputE = e.srcElement || e.target;
        inputE.setAttribute('value', inputE.value);
        if (inputE.value == "") {
          inputE.style.borderBottom = "1px solid #FBB03B";
          inputE.parentNode.style.color = "#FBB03B";
        } else {
          inputE.style.borderBottom = "1px solid #000000";
          inputE.parentNode.style.color = "#000000";
        }
      });
    }
  }
}
