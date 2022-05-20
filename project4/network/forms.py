from django import forms

from .models import *


class post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = {

            "data",

        }
        widgets = {
            "data": forms.Textarea(attrs={"class": "form-control form-control-lg", "placeholder": "Post here!", "cols": "5", "rows": "6"}),
        }
