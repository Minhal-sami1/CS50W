from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name = "index"),
    #API Route
    path("sections/<int:id>", views.sections, name = "section")
]