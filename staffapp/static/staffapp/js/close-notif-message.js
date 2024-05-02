const message = document.getElementsByClassName("error-message");
const closebutton = document.getElementsByClassName("close-error-message");

for (let i = 0; i < message.length; i++) {
    for (let i = 0; i < closebutton.length; i++) {
        closebutton[i].onclick = function () {
            message[i].style.display = "none";
        }
    }
}