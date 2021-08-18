import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

def index(request):
    return render(request, "network/index.html")


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
            user = User.objects.create_user(username, email, password,name=name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


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
                print("error saving the post")
                return render(request, "network/create.html", {
                    "message" : "Error saving the post."
                })
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/create.html")

# Retrieve posts for given user id. If userid=-1 all posts will be retrieved.
def posts(request, userid, following = 0):
    print(f"following value {following}, userid {userid}")
    print(type(following))
    #Filter posts of user (if any) or retrieve all the posts
    if userid != "-1" and following == 0:
        try:
            posts = Post.objects.filter(author=User.objects.get(id=int(userid)))
        except:
            return render(request, "network/404.html", {
                "message" : "The user you are trying to reach does not exist."
            })
    else:
        if following == 1:
            try:
                print("enters")
                user = request.user
                print(user)
                following_users = user.following.all()
                posts = Post.objects.filter(author__in=following_users)
            except:
                return render(request, "network/404.html", {
                "message" : ""
            })
        else: 
            posts = Post.objects.all()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

    
# Retrieve user info for profile
def profile_info(request, userid):
    following = None
    try:
        userid = int(userid)
        user = User.objects.get(id=userid)

        current_user = request.user
        if current_user.is_authenticated:
            if current_user.id != userid:
                if current_user in user.followers.all():
                    following = True
                else:
                    following = False
    except:
        return render(request, "network/404.html", {
            "message" : "The user you are trying to reach does not exist."
        })
    if request.method == "GET":
        return JsonResponse({"user": user.serialize(), "following": following }, safe=False)


def profile(request, userid):
    if request.method == "GET":
        # info = profile_info(request, userid)
        # return render(request, "network/index.html", {
        #     "info": json.loads(info.content),
        # })
        return HttpResponse(status=204)
    elif request.method == "PUT":
        userid = int(userid)
        user = User.objects.get(id=userid)

        data = json.loads(request.body)
        follow = data.get("follow")
        if follow is not None:
            if follow == True:
                user.followers.add(request.user)
            elif follow == False:
                user.followers.remove(request.user)
        user.save()
        return HttpResponse(status=204)

@login_required
def following(request):
    user = request.user
    if request.method == 'GET':
        if user.is_authenticated:
            post = Post(author=user, content=request.POST["content"])
            try:
                post.save()
                return HttpResponseRedirect(reverse("index"))
            except:
                print("error saving the post")
                return render(request, "network/create.html", {
                    "message" : "Error saving the post."
                })
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/create.html")