
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("following", views.following, name="following"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path("display_posts/<str:set>", views.display_posts, name="display_posts"),
    path("user/<int:profile_id>", views.user, name="user"),


    # API paths
    path("posts/<str:set>", views.posts, name="posts"),
    path("posts/user/<int:user_id>", views.user_posts, name="user_posts"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("post/<int:id>", views.post, name="register"),
    path("is_following", views.is_following, name="is_following"),
    path("likes", views.likes, name="likes"),

]
