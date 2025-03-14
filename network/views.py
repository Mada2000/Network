from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
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
    
    # if the user isn't signed in redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    # get all the posts
    all_posts = Post.objects.all()

    # get all the user's liked posts 
    user_liked_post_list = Follower.objects.get(user=request.user).liked_posts.all()
    return render(request, "network/index.html", {
        "posts": all_posts,
        "user_liked_post_list" : user_liked_post_list
    })

def profile(request):
    user_stats = Follower.objects.get(user = request.user)

    return render(request, "network/profile.html", {
        "user_stats" : user_stats
    })

def user_profile(request, username):
    user_stats = Follower.objects.get(user__username = username)
    user_posts = Post.objects.filter(post_username__username=username).all()
    main_user_liked_post_list = Follower.objects.get(user=request.user).liked_posts.all()


    return render(request, "network/user_profile.html", {
        "user_stats" : user_stats,
        "user_posts" : user_posts,
        "main_user_liked_post_list" : main_user_liked_post_list
    })


#ToDO: the javascript function to follow a user gets an error and the follow function doesn't work
#need to modify user_profile.html and the follow function in posts.js to make it work
@csrf_exempt
def follow(request, username):
    if request.method == 'POST':
        # add new follower to the followers list and increase the followers by 1
        new_follower = Follower.objects.get(user__username=username)
        new_follower.followers_list.add(new_follower)
        new_follower.followers_count += 1

        # Save the changes
        new_follower.save()

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
            user_activity = Follower(user = user, following_count = 0, followers_count = 0)
            user_activity.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
