from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.get_profile, name="profile"),
    # API ROUTES
    path("following/", views.following_post, name="get_follow"),
    path("dolike/<int:liker>/<int:post>/",
         views.do_like, name="like"),
    path("dofollow/<int:follower>/<int:following>/<str:status>",
         views.do_follow, name="follow"),
    path("editpost/<int:post_id>/", views.edit_post, name="editpost"),
    path("getposts/", views.get_post, name="get_post"),
    path("post/", views.post, name="post")
]
