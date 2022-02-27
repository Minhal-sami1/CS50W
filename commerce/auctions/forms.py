from django import forms

from .models import *

class listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = {
            "name",
            "category",
            "image",
            "description",
            "first_bid",

        }
        widgets = {
             "name": forms.TextInput(attrs = {"class": "form-control form-control-lg", "placeholder" : "Name of the product here!", "autocomplete": "off", "autofocus" : "on" }),
             "category": forms.Select(attrs = {"class": "form-control form-control-lg"}),
             "image": forms.FileInput(attrs = {"class": "form-control form-control-lg"}),
             "description": forms.Textarea(attrs = {"class": "form-control form-control-lg", "placeholder" : "Description here!"}),
             "first_bid": forms.NumberInput(attrs = {"class": "form-control form-control-lg", "placeholder" : "First Bid here!"})
             }
class bid_form(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = {
                "bid"
                }
        widgets = {
                 "bid": forms.NumberInput(attrs = {"class": "form-control form-control-lg", "placeholder" : "Bid here!"})
                 }

class comments_form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {
                "comment"
                }
        widgets = {
                 "comment": forms.Textarea(attrs = {"class": "form-control form-control-lg", "placeholder" : "Your Value-able Comments!"})
                 } 