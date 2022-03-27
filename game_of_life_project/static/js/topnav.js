function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav" || x.className==="topnav_right") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}