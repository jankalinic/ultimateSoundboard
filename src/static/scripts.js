function pastebin(){
//TODO: REPLACE SSH COMMAND
    var text = "sshpass -p 'YourPassword' ssh user@host";

    navigator.clipboard.writeText(text).then(function() {
      console.log('Async: Copying to clipboard was successful!');
    }, function(err) {
      console.error('Async: Could not copy text: ', err);
    });
}

//create folder
var createfolder_form = document.getElementById("createfolder");
document.getElementById("submitfolder").addEventListener("click", function () {
  createfolder_form.submit();
});

//search
var search_form = document.getElementById("search_form");
document.getElementById("submitsearch").addEventListener("click", function () {
  search_form.submit();
});

// player
function vzp(path) {
    $.ajax({
      url: "/vzp-send.py",
      type: "POST",
      data: path,
      dataType: "text"
    });
}