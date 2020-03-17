from django import forms

from .models import Data

class PostForm(forms.ModelForm):
    class Meta:
        model = Data
        fields= [
            "sub_category",
            "spent",
            "recursive",
            "pay_type",
        ]
