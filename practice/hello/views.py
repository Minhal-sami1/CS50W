from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request, name=None):
    if name:
        return render(request, "hello/test.html", {
            "name": name.capitalize()
        })
    return render(request, "hello/index.html")


def date(request):
    now = datetime.now()
    return render(request, "hello/date.html", {
        "date": now,
        "birthday": now.day == 27 and now.month == 6
    })


def test(request, name):
    return index(request, name)
    # return HttpResponse("Hello, {}!!!".format(name.capitalize()))
