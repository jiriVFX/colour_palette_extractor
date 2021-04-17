function Copy(colourID) {
    var colourCode = document.getElementById(colourID);
    colourCode.select();
    document.execCommand("copy");
    //alert("Copied to clipboard: " + colourCode.value);
}