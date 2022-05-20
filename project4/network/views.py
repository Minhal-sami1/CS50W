from http.client import HTTPSConnection
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import post_form
from .models import Followers, Likes, User, Post
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import json


def index(request):
    user_value = 0
    if request.user.is_authenticated:
        user_value = 1
    posts = Post.objects.order_by("id").reverse()
    like_posts = {}
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    for post in page_obj:
        like = len(post.get_likes())
        like_posts[post.id] = like
    return render(request, "network/index.html", {
        "form": post_form,
        "page_obj": page_obj,
        "user_value": user_value,
        "likes_posts": like_posts
    })


def following_post(request):
    if request.user.is_authenticated:
        likes_posts = {}
        try:
            following = Followers.objects.filter(follower=request.user)
        except Followers.DoesNotExist:
            following = None
        if following != None:
            posts = []
            for follow in following:
                try:
                    page = Post.objects.filter(owner=follow.following)
                    for post in page:
                        posts.append(post)
                except Post.DoesNotExist:
                    pass
        posts.reverse()
        for post in posts:
            like = len(post.get_likes())
            likes_posts[post.id] = like
        paginator = Paginator(posts, 10)
        p = request.GET.get('page')
        page_obj = paginator.get_page(p)
        print(likes_posts)
        return render(request, "network/following.html", {
            "page_obj": page_obj,
            "likes_posts": likes_posts
        })


def get_like(request, liker, post):
    try:
        user_id = User.objects.get(id=liker)
        post_id = Post.objects.get(id=post)
        like_check = Likes.objects.get(liker=user_id, liketo=post_id)
    except (User.DoesNotExist, Post.DoesNotExist, Likes.DoesNotExist) as error:
        like_check = None
    if like_check != None:
        return JsonResponse({"already": "TRUE"})
    else:
        return JsonResponse({"already": "FALSE"})


def do_like(request, liker, post):
    if request.method == "GET":
        return get_like(request, liker, post)
    elif request.method == "PUT":
        message = json.loads(request.body)
        try:
            user_id = User.objects.get(id=liker)
            post_id = Post.objects.get(id=post)
        except (User.DoesNotExist, Post.DoesNotExist, Likes.DoesNotExist) as error:
            return JsonResponse({"message": "There is some wrong information"})
        if message == "LIKE":
            like = Likes(liker=user_id, liketo=post_id)
            like.save()
            return JsonResponse({"message": "Successfully Liked!"})
        elif message == "UNLIKE":
            like = Likes.objects.get(liker=user_id, liketo=post_id)
            like.delete()
            return JsonResponse({"message": "Successfully UnLiked!"})
    pass


def get_profile(request, id):
    user = User.objects.get(id=id)
    followers = Followers.objects.filter(following=user)
    posts = Post.objects.filter(owner=user).order_by("id").reverse()
    following = Followers.objects.filter(follower=user)
    likes_posts = {}
    for post in posts:
        like = len(post.get_likes())
        likes_posts[post.id] = like

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    if request.user == user:
        follow_do = "SAME"
    else:
        try:
            follow_do = Followers.objects.get(
                following=user, follower=request.user)
        except Followers.DoesNotExist:
            follow_do = "NONE"
    print(page_obj)
    return render(request, "network/user.html", {
        "followers": len(followers),
        "following": len(following),
        "page_obj": page_obj,
        "id_user": user,
        "follow_do": follow_do,
        "likes_posts": likes_posts
    })


def do_follow(request, follower, following, status):
    user_follower = User.objects.get(id=int(follower))
    user_following = User.objects.get(id=int(following))
    if(user_follower == user_following):
        return JsonResponse({"message": "ERROR"})
    if (status == "follow"):
        f = Followers(follower=user_follower, following=user_following)
        f.save()
        return JsonResponse({"message": "Unfollow"})
    else:
        f = Followers.objects.get(
            follower=user_follower, following=user_following)
        f.delete()
        return JsonResponse({"message": "Follow"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user'] = 1
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    request.session['user'] = 0
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        request.session['user'] = 1
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def get_post(request):
    if request.method == "GET":

        start = int(request.GET.get("start") or 0)
        end = int(request.GET.get("end") or (start + 9))
        try:
            posts = Post.objects.order_by("id")[start:end]

        except (Post.DoesNotExist, ValueError) as error:
            return JsonResponse({
                "ENDED": "ENDED"
            })
        object_json = {}
        for data in reversed(posts):
            post = str(data.data)
            owner = str(data.owner)
            date = str(data.date)
            owner_id = data.owner.id
            object_json[data.id] = [owner_id, owner, post, date]
        if object_json != {}:
            return JsonResponse(object_json)
        else:
            return JsonResponse({"ENDED": "ENDED"})


def post(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        form = Post(data=data, owner=request.user)

        if len(data) <= 300:
            form.save()
            return JsonResponse({
                "message": "Successfully Made the post!"}, status=201)
        else:
            return JsonResponse({
                "message": "Post written more than the limit!!"
            }, status=200)


def edit_post(request, post_id):
    if request.method == "POST":
        try:
            editpost = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"message": "Post Not Found!"})
        if editpost != None:
            contents = json.loads(request.body)
            editpost.data = contents
            editpost.save()
            return JsonResponse({"message": "Post Edited Successfully!"})

        pass
