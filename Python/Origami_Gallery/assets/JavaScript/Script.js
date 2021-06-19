function changeLanguage() {
	var lang = document.getElementById("language").value;
	var en = document.getElementsByClassName("en")
	var pt = document.getElementsByClassName ("pt")
	if (lang=="en"){
		for (i = 0; i<en.length; i++){
				en[i].style.display = "block"
				pt[i].style.display = "none"
		}
	}
	else{
		for (i = 0; i<en.length; i++){
				en[i].style.display = "none"
				pt[i].style.display = "block"
		}
	}
}

function randomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

document.addEventListener("DOMContentLoaded", function(event) {
	var elems = document.querySelectorAll('.photo_frame');
    var index = 0, length = elems.length;
    for ( ; index < length; index++) {
        elems[index].style.transform = "rotate("+randomNumber(-10, 10)+"deg)";
    }
});
