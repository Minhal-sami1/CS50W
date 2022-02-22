from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/<str:name>", views.test, name="test"),
    path("date", views.date, name="date")
]
