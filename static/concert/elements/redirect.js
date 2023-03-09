function copyStringToClipboard (str) {
    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = str;
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');
    // Remove temporary element
    document.body.removeChild(el);
    }
function getOut() {
    location.href = url;

}
const menuButton = document.getElementById("menu-button");
const menu = document.getElementById("menu");
const sleep = ms => new Promise(r => setTimeout(r, ms));
var i = false;
let style = window.getComputedStyle(menuButton);
var visibility = style.getPropertyValue('visibility');
console.log(visibility);
if (visibility == "hidden") {
    setTimeout(getOut, 2000);
}
else {
    menuButton.addEventListener("click", function(event) {
    if (i == false) {
        event.preventDefault();
        menu.style.display = "flex";
        copyStringToClipboard(url);
        i = true;
        setTimeout(getOut, 20000);
      }})}
if (menuButton == null) {
    setTimeout(getOut, 2000);
  }
  








