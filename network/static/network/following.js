document.addEventListener('DOMContentLoaded', function () {
    // Load all posts by default
    load_posts("following")
})

async function load_posts(set) {
    // fetch(`/display_posts/${set}`)
    // .then(response => response.text())
    // .then(data => document.querySelector("#posts-view").innerHTML=data);

    page_number = document.querySelector("#page-number").value;
    response = await fetch(`/display_posts/${set}?page=${page_number}`);
    data = await response.text();
    document.querySelector("#posts-view").innerHTML=data;
}
