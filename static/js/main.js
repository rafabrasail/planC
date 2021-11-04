var buttonModalCreatePost = document.getElementById('buttonModal')
var modalCreatePost = document.getElementById('createPostModal')
var closeCreatePost = document.getElementsByClassName('delete')[0]

buttonModalCreatePost.onclick = function() {
    modalCreatePost.style.display = 'block'
}

closeCreatePost.onclick = function() {
    modalCreatePost.style.display = 'none'
}

window.onclick = function(event) {
    if(event.target.className == 'modal-background'){
        modalCreatePost.style.display = 'none'
    }
}
