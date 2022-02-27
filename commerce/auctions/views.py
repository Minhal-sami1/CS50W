from distutils.log import error
from urllib.parse import uses_relative
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import *

def index(request):
    listings = Listing.objects.filter(status = True)
    return render(request, "auctions/index.html", {
        "data": listings
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def new_product(request):
    if request.method == "POST":
        form = listing_form(request.POST, request.FILES)
        already_present = Listing.objects.filter(name = request.POST["name"])
        form.instance.owner = request.user
        if form.is_valid() and not already_present:
            form.instance.owner = request.user
            form.save()
            return render(request, "auctions/new-product.html",{
                "form": listing_form,
                "success": "Completed Successfully!!"
            })
        else:
            return render(request, "auctions/new-product.html",{
                "form": listing_form,
                "message": form.errors
            })


    if request.method != "POST":
        return render(request, "auctions/new-product.html",{
            "form": listing_form,
            "error": "Something is not right!"
        })

@login_required(login_url="login")
def change_listing(request, product_id ,type):
    product = Listing.objects.get(id = product_id)

    if type == "bid":
        form = bid_form(request.POST)
        form.instance.user = request.user
        form.instance.listing = product
        data = Bidding.objects.filter(listing = product_id)
            
        current_bid = 0
        for bid in data:
            comp = float(bid.bid)
            if comp > float(current_bid):
                current_bid = comp
        

        if current_bid >= float(request.POST["bid"]) and not form.is_valid():
            error="The bid is lower than or equal to the previous one"
            return redirect(reverse("message", args=("error", error)))

        else:
            form.save()
            success="The bid has been made"
            return redirect(reverse("message", args=("success", success)))
    
    elif type == "comment":
        form = comments_form(request.POST)
        form.instance.user = request.user
        form.instance.listing = product
        if form.is_valid():
            form.save()
            success = "Commented"
            return redirect(reverse("message", args=("success", success)))
        else:
            error = f"There is some problem!!"
            return redirect(reverse("message", args=("error", error)))
    elif type == "watchlist":
        
        try:
            user = User.objects.get(username = request.user)
        except User.DoesNotExist:
            user = None    
        
        watch = Watchlist.objects.filter(listing = product_id, user = user).first()
        if not watch:
            watch = Watchlist(listing = product, user = user)
        status = watch.Status
        if status:
            watch.Status = False
            watch.save()
            return redirect(reverse("listing", args=(product_id,)))
        else:
            watch.Status = True
            watch.user = user
            watch.save()
            return redirect(reverse("listing", args=(product_id,)))
    
    elif type == "close":
        product.status = False
        product.save()
        return redirect(reverse("message", args=("success", "Listing has been closed!")))
    pass


def message(request, type, message):
    if type == "success":
        return render(request, "auctions/message.html",{
            "success": message
        })

    elif type == "error":
        return render(request, "auctions/message.html",{
            "error": message
        })



def listing_view(request, product_id, success = None, error = None):
    #try:
    try:
        user = User.objects.get(username= request.user)
    except User.DoesNotExist:
        user = None
    try:
        product = Listing.objects.get(id = product_id)
    except Listing.DoesNotExist:
        return redirect(reverse("message", args=("error", "404, Does not exist!!")))

    all_bid = Bidding.objects.filter(listing = product.id)
    comments = Comments.objects.filter(listing = product.id)
    watch = None
    
    try:
        user = User.objects.get(username = request.user)
    except User.DoesNotExist:
        user = None
    
    watch = Watchlist.objects.filter(listing = product_id, user = user).first()
    if not watch:
        watch = Watchlist(listing = product, user = user)
    
    if watch :
        status = watch.Status
    else:
        status = None    
    #except:
     #   redirect(reverse("index"))
      #  pass
    owner = False
    if product.owner == request.user:
        owner = True
    
    current_bid = 0
    for bid in all_bid:
        comp = float(bid.bid)
        if comp > float(current_bid):
            current_bid = comp

    return render(request, "auctions/listing.html", {
        "product": product,
        "owner": owner,
        "current_bid": current_bid,
        "comments": comments,
        "form": bid_form,
        "comment": comments_form,
        "error": error,
        "success": success,
        "status": status 
    })

@login_required(login_url="login")
def watchlist(request):
    try:
        user = User.objects.get(username = request.user)
    except User.DoesNotExist:
        user = None
    try:
        data = Watchlist.objects.filter(user = user, Status = True)
    except Watchlist.DoesNotExist:
        data = None
    if not data or not user:
        return redirect(reverse("message", args=("error", "No listings")))
    print(data)    
    return render(request, "auctions/watchlist.html", {
        "data": data
    })
