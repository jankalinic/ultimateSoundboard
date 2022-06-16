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

//tts
var tts = document.getElementById("tts");
document.getElementById("submittts").addEventListener("click", function () {
  tts.submit();
});

// player
function play_sound(path) {
    $.ajax({
      url: "/play_sound",
      type: "POST",
      data: {sound_file:path},
      dataType: "text"
    });
}

function stop_sound() {
    $.ajax({
      url: "/stop_sound",
      type: "POST",
      data: "",
      dataType: "text",
      success: function(data){
        console.log(data);
      }
    });
}
function set_volume(volume_choice) {
    $.ajax({
      url: "/set_volume",
      type: "POST",
      data: {volume:volume_choice},
      dataType: "text",
      success: function(data){
        console.log(data);
      }
    });
}
function read(text) {
    $.ajax({
      url: "/stop_sound",
      type: "POST",
      data: {read:text},
      dataType: "text",
      success: function(data){
        console.log(data);
      }
    });
}