/* 
The following code was taken from Materialize CSS to allow certain function to work
*/

// Dropdown Menu
$(document).ready(function(){
  $(".dropdown-trigger").dropdown();
      
});

// Parallax Image 
$(document).ready(function(){
  $('.parallax').parallax();
});

// Pop up Modal
$(document).ready(function(){
  $('.modal').modal();
});

// Collapsible 
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

