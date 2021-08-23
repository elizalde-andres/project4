document.addEventListener('DOMContentLoaded', function () {
    forms = document.querySelectorAll("#edit-form");
    forms.forEach( form => {
        form.style.display = 'none'
    })
    load_liking_functionality();
    load_editing_functionality();
})

async function load_editing_functionality() {
    edit_buttons = await document.querySelectorAll(".edit-btn");
    
    edit_buttons.forEach(button => {

            document.querySelector(`#edit-form-${button.value}`).style.display = 'none';
            document.querySelector(`#post-content-${button.value}`).style.display = 'block';

        button.addEventListener("click", () => {

            post_form = document.querySelector(`#edit-form-${button.value}`)
            post_content = document.querySelector(`#post-content-${button.value}`);

            post_form.style.display = 'block';
            post_content.style.display = 'none';
            button.style.display = 'none'


            document.querySelector(`#content-${button.value}`).innerHTML = post_content.innerText.trim();

            save_btn = document.querySelector(`#save-${button.value}`);
            save_btn.addEventListener("click", async () => {
                content = await document.querySelector(`#content-${button.value}`).value;

                await fetch(`/post/${button.value}`, {
                    method: 'PUT',
                    headers:{'X-CSRFToken': getCookie("csrftoken")},
                    body: JSON.stringify({
                        content: content
                    })
                })
                
                post = await fetch(`/post/${button.value}`)
                post = await post.json()
                
                post_content.innerText = post.content;
                post_form.style.display = 'none';
                post_content.style.display = 'block';
                button.style.display = 'inline';
                
            })
        })
    });
}



async function load_liking_functionality() {

    like_buttons = await document.querySelectorAll(".like-btn");

    like_buttons.forEach(async button => {
        let likes = await fetch('/likes', {
                                method: 'POST',
                                headers:{'X-CSRFToken': getCookie("csrftoken")},
                                body: JSON.stringify({
                                    post_id: button.id
                                })
                            })
        
        likes = (await likes.json())["likes"]

        update_like_button(button, likes);

        button.addEventListener("click", async () => {
            likes = !likes;
            await fetch(`/post/${button.id}`, {
                method: 'PUT',
                headers:{'X-CSRFToken': getCookie("csrftoken")},
                body: JSON.stringify({
                    like: likes
                })
            })

            update_like_button(button,likes);
            update_likes_count(button.id);
        })

    })
}



function update_like_button(button, likes) {
    if (likes) {
        button.classList = ["like-btn fa fa-heart"]
    } else {
        button.classList = ["like-btn fa fa-heart-o"]
    }
}

async function update_likes_count(post_id) {
    post = await fetch(`/post/${post_id}`)
    post = await post.json()
        
    document.querySelector(`#post-like-count-${post_id}`).innerHTML = `${post["likes_count"]}`
}


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }