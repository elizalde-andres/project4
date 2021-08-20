document.addEventListener('DOMContentLoaded', function () {
    // Load all posts by default
    load_posts("following")
})

function load_posts(set) {
    fetch(`/display_posts/${set}`)
    .then(response => response.text())
    .then(data => document.querySelector("#posts-view").innerHTML=data);
}
