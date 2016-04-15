
function showHint(str) {
    if (str.length == 0) {
        document.getElementById("txtHint").innerHTML = "v";
        return;
    } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("txtHint").innerHTML = xmlhttp.responseText;
            }
        };

        xmlhttp.open("GET", "/chemical/substance/search/" + str, true);
        xmlhttp.send();
    }
}

