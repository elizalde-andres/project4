document.addEventListener('DOMContentLoaded', function () {
    const user_id = JSON.parse(document.getElementById('user_id').textContent);

    document.querySelector('#all-posts').addEventListener('click', () => load_posts("-1"));
    document.querySelector('#following').addEventListener('click', () => load_posts(user_id, 1));

    // Load all posts by default
    // if (userid){
    //     load_posts(userid);
    // } else {
    //     load_posts("-1")
    // }
    load_posts("-1")

})

//Loads posts for given user id (all posts if userid=-1) - if following true, filters only posts by following users
async function load_posts(userid, following=0) {
    posts_view = document.querySelector('#posts-view');
    posts_view.innerHTML = ''

    // Show posts view. Hide the rest.
    document.querySelector('#message-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';
    posts_view.style.display = 'block';

    posts = await (await fetch(`/posts/${userid}/${following}`));
    posts = posts.json();
    posts.forEach(post => {      
        //Create div with post info
        // alert(post.author_id)
        const postRow = document.createElement('div');
        postRow.classList.add("row", "post-info");
        postRow.innerHTML = `<div class="col-md-3 align-self-start"><a href="#" id="${post.id}">[${post.author_username}]</a></div>
                              <div class="col-md-6 align-self-start">${post.content}</div> 
                              <div class="col-md-1 align-self-end text-left">${post.likes_count}</div>
                              <div class="col-md-2 align-self-end text-right">${post.timestamp}</div>`;
        posts_view.append(postRow);

        
        document.getElementById(post.id).addEventListener("click", () => {
            load_posts(post.author_id)
            load_profile(post.author_id)
        })

      });
    

    if (userid != "-1" && following == 0) {
        load_profile(userid)
    };
}


async function load_profile(userid) {
    profile_view = document.querySelector('#profile-view');

    profile_view.style.display = 'block';

    profile_info = await (await fetch(`/profile_info/${userid}`)).json()
   
    profile_view.innerHTML = `<div>PROFILE</div>
                            <div id="name">${profile_info.user.name}</div>
                            <div id="username">${profile_info.user.username}</div>
                            <div id="followers">Followers: ${profile_info.user.followers}</div>
                            <div id="following">Following: ${profile_info.user.following}</div>`

    if (profile_info.following != null) {
        const followButton = document.createElement('button');
        followButton.id = "follow"
        if (profile_info.following) {
            followButton.classList = ["unfollow"]
            followButton.innerHTML = "Unfollow"
        } else {
            followButton.classList = ["follow"]
            followButton.innerHTML = "Follow"
        }
        
        followButton.addEventListener("click", async () =>{
            await fetch(`/profile/${userid}`, {
                method: 'PUT',
                headers:{'X-CSRFToken': getCookie("csrftoken")},
                body: JSON.stringify({
                    follow: !profile_info.following
                })
                });
        // Reload profile info after clicking Follow/Unfollow button
        load_profile(userid)
        });
        profile_view.append(followButton);
    }

}


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

