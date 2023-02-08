// When the user clicks the button, open the modal, store this information on the player field level.
function button_click() {
  document.getElementById("myModal").style.display = "block";
  document.getElementById("id_payment_checked").value="Read"
}

// When the user clicks on <span> (x), close the modal
function span_click(){
  let btn = document.getElementById("myBtn")
  document.getElementById("myModal").style.display = "none";
}