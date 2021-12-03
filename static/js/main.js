var buttonCreatePost = document.getElementById('modalCreatePost')
var modalCreatePost = document.getElementById('pageModalCreatePost')
var close = document.getElementsByClassName('delete')[0];
var closeBtn = document.getElementsByClassName('deleteBtn')[0];
const btnSavePost = document.getElementById('btn-save-post')

const alertBox = document.getElementById('alert-box')

const notificationBox = document.getElementsByClassName('notification')
const closeNotification = document.getElementById('close-notification')

const loadBtn = document.getElementById('load-btn')
const endBox = document.getElementById('end-box')

buttonCreatePost.onclick = function() {
  modalCreatePost.style.display = 'block';
}

closeBtn.onclick = function() {
  modalCreatePost.style.display = 'none';
}

close.onclick = function() {
  modalCreatePost.style.display = 'none';
}

btnSavePost.onclick = function() {
  modalCreatePost.style.display = 'none';
}

window.onclick = function(event){
  if(event.target.className == 'modal-background') {
    modalCreatePost.style.display = 'none'
  }
}


const handleAlerts = (type, msg) => {
  alertBox.innerHTML = `
    <div class="notification mb-2 ${type}" id="notification-box">
      <button class="delete" aria-label="close" id="close-notification"></button>
      ${msg}
    </div>  
  `
}

const postDeleted = localStorage.getItem('caption')

if (postDeleted) {
  handleAlerts('is-danger', `deleted "${postDeleted}"`)
  localStorage.clear()
}




