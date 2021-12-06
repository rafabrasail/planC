const spinnerBox = document.getElementById('spinner-box')  // progress bar to load content

const url = window.location.href + "data/"
const updateUrl = window.location.href + "update/"
const deleteUrl = window.location.href + "delete/"

const updateForm = document.getElementById('form-update-post')
const deleteForm = document.getElementById('form-delete-post')

const updateBtn = document.getElementById('update-btn')
const deleteBtn = document.getElementById('delete-btn')

const postBoxDetail = document.getElementById('post_box_detail')
const modalUpdatePost = document.getElementById('pageModalUpdatePost')
const modalDeletePost = document.getElementById('pageModalDeletePost')

var close = document.getElementsByClassName('delete')[0];
var closeBtn = document.getElementsByClassName('deleteBtn')[0];

const closeDeleteModel = document.getElementById('closeModalDeletePost')

const contentInput = document.getElementById('id_content')
const captionInput = document.getElementById('id_caption')
const tagsInput = document.getElementById('id_tags')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const alertBox = document.getElementById('alert-box')

updateBtn.onclick = function() {
    modalUpdatePost.style.display = 'block';
}

deleteBtn.onclick = function() {
    modalDeletePost.style.display = 'block';
}

close.onclick = function() {
  modalUpdatePost.style.display = 'none';
  modalDeletePost.style.display = 'none';
}

window.onclick = function(event){
  if(event.target.className == 'modal-background') {
    modalUpdatePost.style.display = 'none' 
    modalDeletePost.style.display = 'none'
  }
}

// closeBtn.onclick = function() {
//     modalDeletePost.classList.remove(is-active)
// }

// window.onclick = function(event){
//   if(event.target.className == 'deleteBtn') {
//     modalDeletePost.style.display = 'none'
//   }
// }

// window.onclick = function(event){
//   if(event.target.className == 'deleteBtn') {
//     modalUpdatePost.style.display = 'none'
//   }
// }

const handleAlerts = (type, msg) => {
  alertBox.innerHTML = `
    <div class="notification mb-2 ${type}" id="notification-box">
      <button class="delete" aria-label="close" id="close-notification"></button>
      ${msg}
    </div>  
  `
}


$.ajax({
  type: 'GET',
  url: url,
  data: {},
  success: function(response) {
    console.log('response', response)
    const data = response.data

    if (data.logged_in !== data.user) {
        console.log('different')
    } else {
        console.log('the same')
        updateBtn.classList.remove('is-hidden')
        deleteBtn.classList.remove('is-hidden')
    }

    // const titleEl = document.createElement('h3')
    // titleEl.setAttribute('class', 'mt-1')

    // const bodyEl = document.createElement('p')
    // bodyEl.setAttribute('class', 'mt-1')    

    // titleEl.textContent = data.caption

    captionInput.value = data.caption

    spinnerBox.classList.add('is-hidden')
  },
  error: function(error) {
    console.log('error', error)
  }
})


updateForm.addEventListener('submit', e => {
  e.preventDefault()

  const caption = document.getElementById('post-caption')

  $.ajax({
    type: 'POST',
    url: updateUrl,
    data: {
      'csrfmiddlewaretoken': csrf[0].value,
      // 'caption': captionInput.value,       voltar depois de resolver o post form
    },
    success: function(response) {
      console.log('response', response)
      handleAlerts('is-primary', 'Post has been updated')
      caption.textContent = response.caption
      $('#btn-update-post').click(function() {
        $('#pageModalUpdatePost').removeClass("is-active");
      });
    },
    error: function(error) {
      console.log('error', error)
    }
  })
})


deleteForm.addEventListener('submit', e => {
  e.preventDefault()

  $.ajax({
    type: 'POST',
    url: deleteUrl,
    data: {
      'csrfmiddlewaretoken': csrf[0].value,
    },
    success: function(response) {
      console.log('response', response)
      window.location.href = window.location.origin
      // localStorage.setItem('caption', captionInput.value)     voltar depois de resolver post form
    },
    error: function(error) {
      console.log('error', error)
    }
  })
})