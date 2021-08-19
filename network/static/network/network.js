document.addEventListener('DOMContentLoaded', function () {
    // Load all posts by default
    load_posts("all")
})

function load_posts(set) {
    fetch(`/posts/${set}`) // or whatever url you assign to that view
    .then(response => response.text())
    .then(data => document.querySelector("#posts-view").innerHTML=data);
}
