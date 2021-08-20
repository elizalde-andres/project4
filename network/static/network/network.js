document.addEventListener('DOMContentLoaded', function () {
    // Load all posts by default
    load_posts("all")
})

async function load_posts(set) {
    page_number = document.querySelector("#page-number").value;
    response = await fetch(`/display_posts/${set}?page=${page_number}`);
    data = await response.text();
    document.querySelector("#posts-view").innerHTML=data;
}