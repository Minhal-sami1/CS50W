import secrets
from turtle import title
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from markdown2 import markdown
from . import util

"""Uses of the Util.py Functions
 util.list_entries() is used to get all the list of the entries made 
 util.get_entry() is used to get all the data related to the string provided in the parameter
 util.save_entry() is used to save a entry as MARKDOWN file
"""


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    # * If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
    # * If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
    # * Clicking on any of the entry names on the search results page should take the user to that entry’s page.
    if request.method == "POST":
        search = request.POST["q"]
        data_get =  util.list_entries()
        lst = []
        for each in data_get:
            
            if search == each:
                return redirect(reverse("get_entry", args=(each, )))
            
            if search.lower() in each.lower():
                lst.append(each)

        return render(request, "encyclopedia/search.html", {
            "list": lst,
            "search" : search
        })
    pass

def get_entries(request, title):
    data = util.get_entry(title)
    avd = False
    data_html = "BLAH"
    try:
        data_html = markdown(data)
        avb = True
    except:
        avb = False
    return render(request, "encyclopedia/get_entry.html", {
        "title": title,
        "data": data_html,
        "avb": avb
    })

def create(request):

    if request.method != "POST":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        description = request.POST["description"]
        title = request.POST["title"]
        check_same = util.get_entry(title)
        if not title or not description or check_same:
            return render(request, "encyclopedia/create.html",{
                "error":"Something is missing or already present"
            })
        else:
            util.save_entry(title, description)
            return redirect(reverse("get_entry", args=(title, )))
  
def edit(request, search):
    if request.method != "POST":
        entry = util.get_entry(search)
        return render(request,"encyclopedia/edit.html",{
            "title": search,
            "entry": entry
        })
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        util.save_entry(title, description)
        return redirect(reverse("get_entry", args=(title, )))

def random(request):
    entries = util.list_entries()
    rand = secrets.choice(entries)
    return redirect(reverse("get_entry", args=(rand,)))