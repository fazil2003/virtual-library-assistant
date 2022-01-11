/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    document.getElementById("close_button").style.display="block";
    document.getElementById("open_button").style.display="none";
    document.getElementById("body").style.opacity="0.8";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("close_button").style.display="none";
    document.getElementById("open_button").style.display="block";
    document.getElementById("body").style.opacity="1";
}