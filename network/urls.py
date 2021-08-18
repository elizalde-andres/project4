
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API paths
    path("posts/<str:set>", views.posts, name="posts"),
    path("posts/user/<int:user_id>", views.user_posts, name="user_posts"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("post/<int:id>", views.post, name="register")
]
