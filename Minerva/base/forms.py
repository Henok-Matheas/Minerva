from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review"]
        exclude = ["review"]
  
class MaterialForm(forms.ModelForm):
  
    class Meta:
        model = Material
        fields = "__all__"
        exclude = ["host", "thumbnail","course", "type", "count", "rating"]

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", 'last_name', 'email', "password1", 'password2']