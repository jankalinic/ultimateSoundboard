function pastessh() {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val("sshpass -p excelent ssh root@ilovework.usersys.redhat.com").select();
  document.execCommand("copy");
  $temp.remove();
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
function play_sound(path) {
    $.ajax({
      url: "/play_sound",
      type: "POST",
      data: {sound_file:path},
      dataType: "text",
      success: function(data){
        console.log(data)
      },
      error: function(data){
        console.log(data)
      }
    });
}