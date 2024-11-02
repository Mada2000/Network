from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post_username = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    post_content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    def __str__(self):
        return f"{self.id}: {self.post_username}"
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers_list = models.ManyToManyField(User, related_name="followers")
    following_list = models.ManyToManyField(User, related_name="following")
    following_count = models.IntegerField()
    followers_count = models.IntegerField()
    liked_posts = models.ManyToManyField(Post, related_name='liked_list')
    def __str__(self):
        return f"{self.id}"