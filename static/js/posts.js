const postsBox = document.getElementById('posts-box')      // div to load posts
const spinnerBox = document.getElementById('spinner-box')  // progress bar to load content

// const newPostForm = document.getElementById('form-newpost')
// const files = document.getElementById()
// const content = document.getElementById()
// const user = document.getElementById()


const getCookie =(name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const likeUnlikePosts = ()=> {
    const likeUnlikeForms = [...document.getElementsByClassName('like-unlike-forms')]
    likeUnlikeForms.forEach(form=> form.addEventListener('submit', e=>{
        e.preventDefault()
        const clickedId = e.target.getAttribute('data-form-id')
        const clickedBtn = document.getElementById(`like-unlike-${clickedId}`)
        console.log('like-unlike')
        $.ajax({
            type: 'POST',
            url: "/like-unlike/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'pk': clickedId,
            },
            success: function(response){
                console.log('response', response)  //for debug
                clickedBtn.textContent = response.liked ? `Unlike (${response.count})` : `like (${response.count})`
            },
            error: function(error){
                console.log('error', error)        //for debug
            }
        })

    }))
}



const getData = () => {
    $.ajax({
        type: 'GET',
        url: '/posts/',
        success: function(response){
            console.log('response', response)
            const data = response.data
            setTimeout(() => {
                spinnerBox.classList.add('not-visible')
                console.log(data)
                data.forEach(element => {
                    postsBox.innerHTML += `
                    <div class="card mb-1">
                        <div class="card-content">
                            <div class="media">
                                <div class="media-left">
                                    <figure class="image is-48x48">
                                        <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" class="is-rounded">
                                    </figure>
                                </div>
                                <div class="media-content">
                                    <p class="title is-4">${element.user}</p>
                                    <time datetime="2016-1-1">${element.posted}</time>
                                </div>                        
                            </div>
                        </div>
        
                        <div class=""card-image>
                            <figure class="image is-4by3">
                                <img src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image">
                            </figure>                
                        </div>
        
                        <div class="card-content">
                            <div class="content">
                                ${element.caption}
                            </div>
                        </div>
        
                        <div class="card-footer">
                            <div class="card-footer-item">
                                <form class="like-unlike-forms" data-form-id="${element.id}">
                                    <button href="#" class="button is-white" id="like-unlike-${element.id}">
                                        ${element.liked ? `Unlike (${element.count})` : `Like (${element.count})`}
                                    </button>
                                </form>
                            </div>
                            <div class="card-footer-item">comment</div>
                            <div class="card-footer-item">share</div>
                            <div class="card-footer-item">send</div>
                        </div>
        
                    </div>
                    `
                });
                likeUnlikePosts()
            }, 1000) //setTimeout()
        },
        error: function(error){
            console.log('error', error)
        }
    })
}

getData()