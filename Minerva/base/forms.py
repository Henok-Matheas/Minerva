from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
  
class MaterialForm(forms.ModelForm):
  
    class Meta:
        model = Material
        fields = "__all__"
        exclude = ["host", "thumbnail", "type"]

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", 'last_name', 'email', "school" , 'year', 'semester' , "password1", 'password2']