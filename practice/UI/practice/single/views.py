from django.http import Http404, HttpResponse
from django.shortcuts import render
import random

# Create your views here.
def index(request):
    return render(request, "single/index.html")

texts = ["Text 1", "NOPE THIS IS DIFFERENT", "Text 3"]

#API View
def sections(request, id):
    if 1 <= id and 3 >= id:
        text = random.random()
        return HttpResponse(text)
    else:
        return Http404("No Such Sections!")