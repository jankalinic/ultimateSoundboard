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

//text to speech
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

function search_filter() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('search_input');
  filter = input.value.toUpperCase();
  ul = document.getElementById("search_area");
  console.log("Search UL: " + ul);
  li = ul.getElementsByClassName('search_card_name');
  console.log("Search LI: " + li);

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    console.log("I: " + li);
    a = li[i].getElementsByClassName("sound_name");
    b = li[i].getElementsByClassName("sound_name")[0];
    console.log("A[0]:" + a);
    console.log("B:" + b);
    txtValue = a.textContent || a.innerText;
    console.log("txtValue: " + txtValue);
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}