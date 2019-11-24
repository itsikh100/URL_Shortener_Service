function confirminput() {
  url = document.getElementById("URLtxt").value;
  alert("The URL " + url + " is now in proccess to get Shor URL");
}

function copyToClipboard() {
  var copyText = document.getElementById('URLtxt');
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand('copy');
  alert("Copied the text: " + copyText.value);
}

function selectionChanged() {
  var x = document.getElementById("selection").value;
  document.getElementById("labelToShow").innerHTML = "You selected: " + x;
}
