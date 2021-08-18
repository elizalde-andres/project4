from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.fields import BooleanField, CharField, DateTimeField, DecimalField, TextField, URLField


class User(AbstractUser):
    name = CharField(max_length=64)
    followers = models.ManyToManyField("User", related_name="following")

    def serialize(self):
        return {
            "id": self.pk,
            "username": "@" + self.username,
            "name": self.name,
            "followers": self.followers_count,
            "following": self.following_count,
        }
    
    def __str__(self):
        return f"{self.username}"

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = DateTimeField(auto_now_add=True, editable=False)
    content = TextField()
    likes = models.ManyToManyField(User, default=0, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author.pk,
            "author_username": "@" + self.author.username,
            "author_name": self.author.name,
            "timestamp": self.timestamp,
            "content": self.content,
            "likes_count": self.likes_count
        }

    def __str__(self) -> str:
        return f"[{self.author}] {self.content}"
    
    @property
    def likes_count(self):
        return self.likes.all().count()
