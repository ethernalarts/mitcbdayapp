
function myFunction() {
	var mobilemenu = document.querySelector('#mobile-menu');
	var x_icon = document.querySelector('#x-icon');
	var hamburger_icon = document.querySelector('#hamburger-icon');

	if (mobilemenu.style.display === "block") {
		mobilemenu.style.display = "none";
		hamburger_icon.style.display = "block";
		x_icon.style.display = "none";
	} else {
		mobilemenu.style.display = "block";
		hamburger_icon.style.display = "none";
		x_icon.style.display = "block";
	}
}