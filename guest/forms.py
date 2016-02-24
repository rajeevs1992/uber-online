from django import forms
from django.forms import PasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=PasswordInput())
