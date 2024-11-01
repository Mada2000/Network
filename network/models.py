from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post_username = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    post_content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers_list = models.ManyToManyField(User, related_name="followers")
    following_list = models.ManyToManyField(User, related_name="following")
    following_count = models.IntegerField()
    followers_count = models.IntegerField()