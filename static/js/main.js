var buttonCreatePost = document.getElementById('modalCreatePost')
var modalCreatePost = document.getElementById('pageModalCreatePost')
var close = document.getElementsByClassName('delete')[0];
var closeBtn = document.getElementsByClassName('deleteBtn')[0];

buttonCreatePost.onclick = function() {
  modalCreatePost.style.display = 'block';
}

closeBtn.onclick = function() {
  modalCreatePost.style.display = 'none';
}

close.onclick = function() {
  modalCreatePost.style.display = 'none';
}

window.onclick = function(event){
  if(event.target.className == 'modal-background') {
    modalCreatePost.style.display = 'none'
  }
}


