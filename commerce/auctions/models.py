from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

# Models: Your application should have at least three models in addition to the User model: 
#       one for auction listings, one for bids, and one for comments made on auction listings. 
# It’s up to you to decide what fields each model should have, and what the types of those fields should be. 
# You may have additional models if you would like.
class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="products_image/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    date = models.DateField(auto_now_add=True)
    first_bid = models.FloatField()
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"ID: {self.id} ,Product: {self.name}, Category: {self.category}, Bid: {self.first_bid}, Date: {self.date}"

class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    bid = models.FloatField()
    date = models.DateField(auto_now_add = True)
    def __str__(self):
        return f"Listing: {self.listing} ; Bid: {self.bid}; Posted by {self.user}"
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    comment = models.CharField(max_length=100)
    date = models.DateField(auto_now_add = True)
    def __str__(self):
        return f"Listing: {self.listing} ; Comment: {self.comment}; Posted by {self.user}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlister")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "watch_list")
    Status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.listing}, Posted By: {self.user}"