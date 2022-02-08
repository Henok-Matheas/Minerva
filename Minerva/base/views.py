from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .forms import *
from .models import *
# Create your views here.

def home(request):
    materials = Material.objects.all()
    return render(request, "base/home.html",{"materials": materials})

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password does not exist")

    context = {"page": page}
    return render(request, "base/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, "base/register.html", {"form": form})


# @login_required(login_url="/login")
def upload(request):
    if request.method == 'POST':
        material = MaterialForm(request.POST, request.FILES)
  
        if material.is_valid():
            material.save()
            return redirect('home')
    else:
        material = MaterialForm()
    return render(request, 'base/upload.html', {'material' : material})


def deleteFile(request,pk):
    material = Material.objects.get(id = pk)
    if request.method == 'POST':
        material.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : material})