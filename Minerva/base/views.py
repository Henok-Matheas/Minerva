from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .forms import *
from .models import *
from .utils import *
# Create your views here.

def home(request):
    materials = Material.objects.all()
    return render(request, "base/home.html",{"materials": materials})

def user(request):
    return render(request, "base/user.html")
    # user = User.objects.get(id = pk)
    # materials = Material.objects.get(school = user.school, year = user.year, semester = user.semester).order_by("rating")
    # return render(request, "base/user.html",{"materials": materials})

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
    
def material(request, pk):
    material = Material.objects.get(id = pk)
    reviews = material.reviews.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.host = request.user
            form.instance.material = material
            form.save()
            return redirect('home')

    context = {'material': material, 'form': form, 'reviews':reviews}
    return render(request, 'base/material.html', context)

# @login_required(login_url="/login")
def upload(request):
    if request.method == 'POST':
        material = MaterialForm(request.POST, request.FILES)
        actual = request.FILES.get('file')
        file_type = fileTypeFinder(actual)
        if material.is_valid():
            mater = Material.objects.create(
                host = request.user,
                name = request.POST.get("name"),
                author = request.POST.get("author"),
                description = request.POST.get("description"),
                course = Course.objects.get(id = 1),
                file = actual,
                type = file_type,
            )
            matrl = Material.objects.get(id = mater.id)
            matrl.thumbnail = thumbnailer(mater.file)
            matrl.type = "video"
            return HttpResponse(matrl.type)
            materl = Material.objects.get(id = material.id)
            materl.thumbnail = thumbnailer(actual)
            return redirect("home")

        # if material.is_valid():
        #     material.save()
        #     return redirect('home')
    else:
        material = MaterialForm()
    return render(request, 'base/upload.html', {'material' : material})


def deleteFile(request,pk):
    material = Material.objects.get(id = pk)
    if request.user != material.host:
        return HttpResponse("You aren't allowed here mate")
    if request.method == 'POST':
        material.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : material})