from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name = "index"),
    #API Route
    path("posts", views.posts, name="posts")
]