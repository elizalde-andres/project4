import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Post, User

def index(request):

    posts = Post.objects.all().order_by("-timestamp")
    posts = [post.serialize() for post in posts]

    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        "posts": page_posts
    })


def following(request):
    following = User.objects.get(pk=request.user.id).following.all()
    posts = Post.objects.filter(author__in=following).order_by("-timestamp")
    posts = [post.serialize() for post in posts]

    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)


    return render(request, "network/following.html", {
        "posts": page_posts
    })
    page = request.GET.get('page')

    return render(request, "network/following.html", {
        "page_number": page
    })
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, name=name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def posts(request, set):
    # Filter posts (all or following)
    if set == "all":
        posts = Post.objects.all()
    elif set == "following":
        posts = Post.objects.filter(author__in=request.user.following.all())
    else:
        return JsonResponse({"error": "Invalid set."}, status=400)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)

# API methods
def user_posts(request, user_id):
    try: 
        posts = User.objects.get(pk=user_id).posts.all().order_by("-timestamp")
        return JsonResponse([post.serialize() for post in posts], safe=False)
    except:
        return JsonResponse({"error": "Invalid user id."}, status=400)

def profile(request,profile_id): 
    try:
        profile_user = User.objects.get(pk=profile_id)
    except:
        return JsonResponse({"error": "Ivalid profile id."}, status=400)
    
    if request.method == "GET":
        return JsonResponse(profile_user.serialize(), safe=False)

    elif request.method == "PUT":
        current_user = request.user
        if current_user.is_authenticated:
            data = json.loads(request.body)
            if data.get("follow") is not None:
                if data.get("follow") == True:
                    profile_user.followers.add(current_user)
                else:
                    profile_user.followers.remove(current_user)
            profile_user.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=403)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def post(request, id):
    try:
        post = Post.objects.get(pk=id)
    except:
        return JsonResponse({"error": "Ivalid post id."}, status=400)

    if request.method == "PUT":
        current_user = request.user
        if current_user.is_authenticated:
            data = json.loads(request.body)
            if data.get("like") is not None:
                if data.get("like") == True:
                    post.likes.add(current_user)
                else:
                    post.likes.remove(current_user)
            if data.get("content") is not None:
                post.content = data["content"]
            post.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=403)
    elif request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)
    else:
        return JsonResponse({
            "error": "PUT or GET request required."
        }, status=400)



@login_required()
def new_post(request):
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            post = Post(author=user, content=request.POST["content"])
            try:
                post.save()
                return HttpResponseRedirect(reverse("index"))
            except:
                return render(request, "network/index.html", {
                    "message" : "Error saving the post.",
                    "content" : request.POST["content"] 
                })
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/index.html")

def display_posts(request, set):
    posts_set = posts(request, set)
    posts_set = json.loads(posts_set.content)

    paginator = Paginator(posts_set,10)
    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)

    return render(request, "network/posts.html", {
        "posts": page_posts
    })


def user(request, profile_id):
    profile_info = profile(request, profile_id)
    profile_info = json.loads(profile_info.content)

    posts = User.objects.get(pk=profile_id).posts.all().order_by("-timestamp")
    posts = [post.serialize() for post in posts]

    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)


    return render(request, "network/profile.html", {
        "profile_info": profile_info,
        "posts": page_posts
    })

def is_following(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user1_id = int(data.get("user1"))
        user2_id = int(data.get("user2"))

        user1 = User.objects.get(pk=user1_id)
        user2 = User.objects.get(pk=user2_id)
        
        is_following = user2 in user1.following.all()        
        return JsonResponse({"is_following": is_following}, safe=False)

def likes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = request.user.id

        post_id = int(data.get("post_id"))

        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)
        likes = user in post.likes.all()
        return JsonResponse({"likes": likes}, safe=False)