from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follower

@csrf_exempt
def decrement_likes(request, post_id):
    if request.method == 'POST':
        # get the selected post by id and decrease the likes count by 1
        post = Post.objects.get(id=post_id)
        post.likes -= 1
        post.save()

        # remove the liked post to the like posts list of the user and save it
        liked_post = Follower.objects.get(user = request.user)
        liked_post.liked_posts.remove(post)
        liked_post.save()
        return JsonResponse({'likes': post.likes})

@csrf_exempt
def increment_likes(request, post_id):
    if request.method == 'POST':
        # get the selected post by id and increase the likes count by 1
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()

        # add the liked post to the like posts list of the user and save it
        liked_post = Follower.objects.get(user = request.user)
        liked_post.liked_posts.add(post)
        liked_post.save()
        return JsonResponse({'likes': post.likes})

def index(request):
    if request.method == "POST":
        #make a new post and add it to the database
        data = request.POST.get("post")
        post_data = Post(post_username = request.user, post_content = data, likes = 0)
        post_data.save()
        return HttpResponseRedirect(reverse("index"))
    
    # get all the posts
    all_posts = Post.objects.all()

    # get all the user's liked posts 
    user_liked_post_list = Follower.objects.get(user=request.user).liked_posts.all()
    return render(request, "network/index.html", {
        "posts": all_posts,
        "user_liked_post_list" : user_liked_post_list
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_activity = Follower(user = request.user, following_count = 0, followers_count = 0)
            user_activity.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
