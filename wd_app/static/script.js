
//this functionality of webpage ends here 

/*
function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "ajax_info.txt", true);
  xhttp.send();
}
*/
//for flashing warning

const warning = document.getElementById('warning');

function warn_hide(){
  document.getElementById('warning').style.display="none";
}

if (warning.innerHTML.length>1){
  setTimeout(warn_hide,5000);
}


//for upload option generation

const upload = document.getElementById('upload-file');
const paste_text = document.getElementById('paste-text');
const enter_url = document.getElementById('webpage-url');
const menu = document.getElementById('menu');
const modal = document.getElementById('modal-text');
const url_input = document.getElementById('url-input');
const upload_menu_op= document.getElementById('upload_menu_option');
const back_button= document.getElementById('back_button');
const text_prompt= document.getElementById('text-prompt');
const always_hide = document.getElementById('always_hide');


function upload_file_menu() {
    document.getElementById("menu").style.display = "block";
    document.getElementById('back_button').style.display="block";
    document.getElementById('text-prompt').style.display="block";
    //value is for setting the request type of flag in the route
    document.getElementById('always_hide').value = "1";
    //options on top are below
    document.getElementById('paste-text').style.display="none";
    document.getElementById('webpage-url').style.display="none";
    document.getElementById('upload-file').style.display="none";
    //options in the menu are below
    document.getElementById('url-input').style.display="none";
    document.getElementById('modal-text').style.display="none";
  }

upload.addEventListener('click',upload_file_menu);


// for paste text option

function paste_text_menu(){
    document.getElementById("menu").style.display = "block";
    document.getElementById('back_button').style.display="block";
    document.getElementById('text-prompt').style.display="block";
    document.getElementById('always_hide').value = "2";
    console.log(always_hide)
    //options in top are below
    document.getElementById('paste-text').style.display="none";
    document.getElementById('webpage-url').style.display="none";
    document.getElementById('upload-file').style.display="none";
    //elements in the menu are below
    document.getElementById('upload_menu_option').style.display="none";
    document.getElementById('url-input').style.display="none";
    document.getElementById('modal-text').style.display="block";
}

paste_text.addEventListener('click',paste_text_menu)


// for url option

function enter_url_func(){
  document.getElementById("menu").style.display = "block";
  document.getElementById('back_button').style.display="block";
  document.getElementById('text-prompt').style.display="block";
  document.getElementById('always_hide').value="3";
  console.log(always_hide)
  //options in top are below
  document.getElementById('paste-text').style.display="none";
  document.getElementById('webpage-url').style.display="none";
  document.getElementById('upload-file').style.display="none";
  //elements in the menu are below
  document.getElementById('upload_menu_option').style.display="none";
  document.getElementById('url-input').style.display="block";
  document.getElementById('modal-text').style.display="none";
}

enter_url.addEventListener('click',enter_url_func)

// func for back button

function for_back_button(){
  //display options in 
  document.getElementById('paste-text').style.display="block";
  document.getElementById('webpage-url').style.display="block";
  document.getElementById('upload-file').style.display="block";
  //hide menu and the back button
  document.getElementById("menu").style.display = "none";
  document.getElementById('back_button').style.display="none";
  document.getElementById('text-prompt').style.display="none";
}

back_button.addEventListener('click',for_back_button)