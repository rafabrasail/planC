// const postsBox = document.getElementById('posts-box')      // div to load posts
const likeBox = document.getElementById('like-box')      // div to load likes
const spinnerBox = document.getElementById('spinner-box')  // progress bar to load content

const newPostForm = document.getElementById('form-newpost')
// const content = document.getElementById('id_content')
// const caption = document.getElementById('id_caption')
// const tags = document.getElementById('id_tags')

const csrf = document.getElementsByName('csrfmiddlewaretoken')
//console.log('csrf', csrf[0].value)

const url = window.location.href

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


// const carousel = () => {
//     const postCarousel = [...document.getElementsByClassName('mySlides')]
//     postCarousel.forEach( () => {
//         console.log('work')
//         var slideIndex = 1;
//         showSlides(slideIndex);

//         // Next/previous controls
//         function plusSlides(n) {
//         showSlides(slideIndex += n);
//         }

//         // Thumbnail image controls
//         function currentSlide(n) {
//         showSlides(slideIndex = n);
//         }

//         function showSlides(n) {
//         var i;

//         if (n > slides.length) {slideIndex = 1}
//         if (n < 1) {slideIndex = slides.length}
//         for (i = 0; i < slides.length; i++) {
//             slides[i].style.display = "none";
//         }

//         slides[slideIndex-1].style.display = "block";

//         }        
//     })
// }


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
                //console.log('response', response)  //for debug
                clickedBtn.textContent = response.liked ? `Unlike (${response.count})` : `like (${response.count})`
                response.forEach(element => {
                    likeBox.innerHTML += `
                        ${element.liked ? `Unlike (${element.count})` : `Like (${element.count})`}
                    `
                });
            },
            error: function(error){
                //console.log('error', error)        //for debug
            }
        })

    }))
}


  var slides = document.getElementsByClassName("mySlides");

const getData = () => {
    $.ajax({
        type: 'GET',
        url: '/posts/',
        success: function(response){
            console.log('response', response)
            const data = response.data
            setTimeout(() => {
                spinnerBox.classList.add('is-hidden')
                console.log(data)
                // data.forEach(element => {
                //     postsBox.innerHTML += ``
                // });
                
                likeUnlikePosts()
            }, 500) //setTimeout()
        },
        error: function(error){
            console.log('error', error)
        }
    })
}


// newPostForm.addEventListener('submit', e => {
//     e.preventDefault()

//     $.ajax({
//         type: 'POST',
//         url: '',
//         data: {
//             'csrfmiddlewaretoken': csrf[0].value,
//             // 'caption': caption.value,
//             // 'tags': tags.value,
//             // 'content': content.value
//         },
//         success: function(response){
//             console.log('response - user', response.user)
//             console.log('response - newPostForm', response)
//             postsBox.insertAdjacentHTML('afterbegin', `
//                 <div class="card mb-1">
//                     <div class="card-content">
//                         <div class="media">
//                             <div class="media-left">
//                                 <figure class="image is-48x48">
//                                     <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" class="is-rounded">
//                                 </figure>
//                             </div>
//                             <div class="media-content">
//                                 <p class="title is-4">${response.user}</p>
//                                 <time datetime="2016-1-1">${response.posted}</time>
//                             </div>                        
//                         </div>
//                     </div>
    
//                     <div class=""card-image>
//                         <figure class="image is-4by3">
//                             <img src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image">
//                         </figure>                
//                     </div>
    
//                     <div class="card-content">
//                         <div class="content">
//                             ${response.caption}
//                         </div>
//                     </div>
    
//                     <div class="card-footer">
//                         <div class="card-footer-item">
//                             <form class="like-unlike-forms" data-form-id="${response.id}">
//                                 <button class="button is-white" id="like-unlike-${response.id}">
//                                     ${response.liked ? `Unlike (${response.count})` : `Like (0)`}
//                                 </button>
//                             </form>
//                         </div>
//                         <div class="card-footer-item">comment</div>
//                         <div class="card-footer-item">share</div>
//                         <div class="card-footer-item">send</div>
//                     </div>
    
//                 </div>            
//             `)
//             likeUnlikePosts()
//             $('#btn-save-post').click(function() {
//                 $('.modal').removeClass("is-active");
//             });
//             handleAlerts('is-primary', 'New post created.')
//             newPostForm.reset()
//         },
//         error: function(error){
//             console.log('error', error)
//             handleAlerts('is-danger is-light', 'Ooops try again.')
//         }
//     })
// })

getData()