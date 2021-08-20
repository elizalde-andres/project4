//(Un)Follow update following and followerss number

document.addEventListener('DOMContentLoaded', function () {
    profile_id = profile_id.text;
    user_id = user_id.text;
    follow_button = document.querySelector("#follow-btn");
    if (follow_button) {
        load_following_functionality(follow_button)
    }
})

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

async function load_following_functionality(follow_button) {

    let is_following = await fetch('/is_following', {
                                method: 'POST',
                                headers:{'X-CSRFToken': getCookie("csrftoken")},
                                body: JSON.stringify({
                                    user1: user_id,
                                    user2: profile_id,
                                })
                            })
    
    is_following = (await is_following.json())["is_following"]

    update_follow_button(is_following);

    follow_button.addEventListener("click", async () => {
        is_following = !is_following;

        await fetch(`/profile/${profile_id}`, {
            method: 'PUT',
            headers:{'X-CSRFToken': getCookie("csrftoken")},
            body: JSON.stringify({
                follow: is_following
            })
        })
        update_follow_button(is_following);

        update_follow_count();
    })

}

function update_follow_button(is_following) {
    if (is_following) {
        follow_button.innerHTML = "Unfollow"
        follow_button.classList.add("btn-unfollow")
    } else {
        follow_button.innerHTML = "Follow"
        follow_button.classList.add("btn-follow")
    }
}

async function update_follow_count() {
    profile = await fetch(`/profile/${profile_id}`)
    profile = await profile.json()
        
    document.querySelector("#follows").innerHTML = `Following: ${profile["following"]} - Followers: ${profile["followers"]}`
}