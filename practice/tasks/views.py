from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import forms
# Create your views here.
tasks = ["foo", "bar", "baz"]


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        data = forms.Tasksform(request.POST)
        if data.is_valid():
            clean = data.cleaned_data["task"]
            request.session["tasks"] += [clean]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": data
            })
    return render(request, "tasks/add.html", {
        "form": forms.Tasksform()
    })
