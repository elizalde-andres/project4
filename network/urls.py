
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_post, name="create"),

    # API routes
    path("posts/<str:userid>/<int:following>", views.posts, name="posts"),
    path("profile/<str:userid>", views.profile, name="profile"),
    path("profile_info/<str:userid>", views.profile_info, name="profile_info"),
]
