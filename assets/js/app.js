function toggleMenu() {
  var x = document.getElementById("navigation");
  if (x.className === "navigation-bar") {
    x.className += " responsive";
  } else {
    x.className = "navigation-bar";
  }
}
