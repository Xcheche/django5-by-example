from django import forms
from .models import *


# Email validation mixin
class EmailValidationMixin:
    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@" not in email:
            raise forms.ValidationError("Invalid email address")
        return email


# Non model form for sharing post
class SharePostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# Comment form


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


# Search form
class SearchForm(forms.Form):
    query = forms.CharField()
