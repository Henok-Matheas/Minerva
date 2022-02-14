import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import F
from  .forms import *
from .models import *
from .utils import *
# Create your views here.

def home(request):
    return render(request, "base/home.html")

@login_required(login_url= "/login")
def userPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    materials = Material.objects.filter(Q(course__semester__name = request.user.semester.name) & Q(course__year__name = request.user.year.name) & Q(course__school__name = request.user.school.name) &
        Q(course__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(type__icontains=q)
    ).order_by("rating")

    most_downloaded = Material.objects.filter(Q(course__semester__name = request.user.semester.name) & Q(course__year__name = request.user.year.name) & Q(course__school__name = request.user.school.name) &
        Q(course__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(type__icontains=q)
    ).order_by("count")

    courses = Course.objects.filter(Q(school__name = request.user.school.name) & Q(year__name = request.user.year.name) & Q(semester__name = request.user.semester.name))
    context = {
        "materials" : materials,
        "user" : request.user,
        "courses" : courses,
        "most_downloaded" : most_downloaded
    }
    return render(request, "base/user.html", context)
    # user = User.objects.get(id = pk)
    # materials = Material.objects.get(school = user.school, year = user.year, semester = user.semester).order_by("rating")
    # return render(request, "base/user.html",{"materials": materials})

def loginPage(request):

    if request.user.is_authenticated:
        return redirect("user")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username is wrong")

        user = User.objects.get(username = "UGR/2553/12", password= "2011")
        if user is not None:
            login(request, user)
            return redirect("user")
        else:
            messages.error(request, "password is incorrect")
    return render(request, "base/login.html")


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("login")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, "base/register.html", {"form": form})


@login_required(login_url="/login")
def upload(request):
    semester = request.user.semester
    courses = semester.course_set.all()
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        actual = request.FILES.get("file")
        file_type = fileTypeFinder(actual)
        if form.is_valid():
            material = form.save(commit=False)
            material.file = actual
            material.host = request.user
            material.type = file_type
            material.course = Course.objects.get(id = request.POST.get("course")) 
            material.save()

            if material.type == "book":
                try:
                    material.thumbnail = re.findall("/thumbnails/.*",str(thumbnailer(actual)))[-1]
                except:
                    material.thumbnail = "thumbnails/book.jpg"
            elif material.type == "video":
              material.thumbnail = "thumbnails/video.jpg"
            else:
                material.thumbnail = "thumbnails/other.jpg"  
            material.save()
            return redirect("user")
        else:
            messages.error(request, "One or more invalid fields")
            return redirect("upload")
    else:
        form = MaterialForm()
    return render(request, 'base/upload.html', {'form' : form, "courses": courses})

@login_required(login_url="/login")
def deleteFile(request,pk):
    material = Material.objects.get(id = pk)
    if request.user != material.host:
        return HttpResponse("You aren't allowed here mate")
    if request.method == 'POST':
        material.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : material})

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q = q.split()

    materials = Material.objects.filter( 
        Q(course__name__icontains__in = q) |
        Q(material__name__icontains = q) |
        Q(material__author__icontains = q)
    )
    context = {"mateials":materials}

    return render(request, 'base/search.html', context)
    
def material(request, pk):
    material = Material.objects.get(id = pk)
    reviews = material.reviews.all()
    ratings = [0,0,0,0,0]
    
    for review in reviews:
        ratings[review.rating-1] += 1
        

    form = None
    user = request.user
    try:
        review = material.reviews.get(host = user)
        form = ReviewForm(instance=review)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review.review = form.instance.review
                ratechange = form.instance.rating - review.rating
                review.rating = form.instance.rating
                
                material.rating = F('rating') + ratechange
                review.save()
                material.save()

                return redirect('home')
        
    except:
        form = ReviewForm()
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.instance.host = request.user
                form.instance.material = material
                material.rating = F('rating') + form.instance.rating
                form.save()
                material.save()

                return redirect('home')

    

    context = {'material': material, 'form': form, 'reviews':reviews, 'ratings':ratings}
    return render(request, 'base/material.html', context)