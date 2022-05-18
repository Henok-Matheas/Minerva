from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from multiprocessing import context
import time
from pathlib import Path
import os.path
from .utils import make_predictions
from django.core.files.storage import FileSystemStorage
import json
from json import JSONDecodeError
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import F
from .forms import *
from .models import *
from .utils import *
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect("user")
    return render(request, "base/home.html")


@login_required(login_url="/login")
def userPage(request):
    if not request.user.is_authenticated:
        return redirect("home")
    user = User.objects.get(username=request.user.username)
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    materials = Material.objects.filter(Q(course__semester__name=user.semester.name) & Q(course__year__name=user.year.name) & Q(course__school__name=request.user.school.name) &
                                        Q(course__name__icontains=q) | Q(name__icontains=q) | Q(
                                            description__icontains=q) | Q(type__icontains=q)
                                        ).order_by("rating")

    most_downloaded = Material.objects.filter(Q(course__semester__name=user.semester.name) & Q(course__year__name=user.year.name) & Q(course__school__name=user.school.name) &
                                              Q(course__name__icontains=q) | Q(name__icontains=q) | Q(
                                                  description__icontains=q) | Q(type__icontains=q)
                                              ).order_by("count")

    courses = Course.objects.filter(
        semester=user.semester, year=user.year, school=user.school)

    # courses = Course.objects.filter(Q(school__name = user.school.name) & Q(year__name = user.year.name) & Q(semester__name = user.semester.name))
    context = {
        "materials": materials,
        "user": request.user,
        "courses": courses,
        "most_downloaded": most_downloaded
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

        user = User.objects.get(username="UGR/2553/12", password="2011")
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
    schools = School.objects.all()
    years = Year.objects.all()
    semesters = Semester.objects.all()
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.school = School.objects.get(id=request.POST.get("school"))
            user.year = Year.objects.get(id=request.POST.get("year"))
            user.semester = Semester.objects.get(
                id=request.POST.get("semester"))
            user.save()
            login(request, user)
            return redirect("login")
        else:
            messages.error(request, "An error occurred during registration")
    context = {
        "form": form,
        "schools": schools,
        "years": years,
        "semesters": semesters,
    }
    return render(request, "base/register.html", context)


@login_required(login_url="/login")
def upload(request):
    semester = request.user.semester
    courses = Course.objects.filter(
        semester=request.user.semester, year=request.user.year, school=request.user.school)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        actual = request.FILES.get("file")
        file_type = fileTypeFinder(actual)
        if form.is_valid():
            material = form.save(commit=False)
            material.file = actual
            material.host = request.user
            material.type = file_type
            material.course = Course.objects.get(id=request.POST.get("course"))
            material.save()

            if material.type == "book":
                try:
                    material.thumbnail = re.findall(
                        "/thumbnails/.*", str(thumbnailer(actual)))[-1]
                except:
                    material.thumbnail = "static/images/book_default.jpg"
            elif material.type == "video":
                material.thumbnail = "thumbnails/video_default.svg"
            else:
                material.thumbnail = "static/images/other_default.svg"
            material.save()
            return redirect("user")
        else:
            messages.error(request, "One or more invalid fields")
            return redirect("upload")
    else:
        form = MaterialForm()
    return render(request, 'base/upload.html', {'form': form, "courses": courses})


@login_required(login_url="/login")
def deleteFile(request, pk):
    material = Material.objects.get(id=pk)
    if request.user != material.host:
        return HttpResponse("You aren't allowed here mate")
    if request.method == 'POST':
        material.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': material})


@login_required(login_url="/login")
def material(request, pk):
    material = Material.objects.get(id=pk)
    reviews = material.reviews.all()
    ratings = [0, 0, 0, 0, 0]
    uReview = None
    for review in reviews:
        ratings[review.rating-1] += 1

    form = None
    user = request.user
    try:
        review = material.reviews.get(host=user)
        uReview = review
        form = ReviewForm(instance=review)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review.review = request.POST.get('review')
                ratechange = form.instance.rating - review.rating
                review.rating = form.instance.rating

                material.rating = F('rating') + ratechange

                review.save()
                material.save()
                return redirect('material', pk=pk)
    except:
        form = ReviewForm()
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.instance.host = request.user
                form.instance.material = material
                form.instance.review = request.POST.get('review')
                material.rating = F('rating') + form.instance.rating
                material.count += 1
                form.save()
                material.save()

                return redirect('material', pk=pk)

    context = {'material': material, 'form': form,
               'reviews': reviews, 'ratings': ratings, 'ureview': uReview}
    return render(request, 'base/material.html', context)


@login_required(login_url="/login")
def userProfile(request):
    user = User.objects.get(username=request.user.username)

    if not user:
        return HttpResponse("YOU ARE NOT ALLOWED HERE.GO BACK!!!!!")

    context = {"user": user}
    return render(request, "user_profile.html", context)


@login_required(login_url="/login")
def updateUser(request):
    user = User.objects.get(username=request.user.username)
    form = MyUserCreationForm(instance=user)

    if request.method == "POST":
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()
            return redirect("user-profile")
        else:
            messages.error(request, "One or more invalid fields")
            return redirect("update-user")
    context = {"form": form,
               "user": user}
    return render(request, "update_user.html", context)


@login_required(login_url="/login")
def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    type = request.GET.get('type') if request.GET.get('type') != None else ''

    materials = Material.objects.filter(Q(type__icontains=type) &
                                         (Q(course__name__icontains=q) |
                                          Q(name__icontains=q) |
                                          Q(author__icontains=q) |
                                          Q(description__icontains=q))
                                        ).order_by("rating")
    context = {
        "materials": materials,
        "query": q}

    return render(request, 'base/search.html', context)


# def home(request):
#     prediction = request.session.get("prediction", False)
#     if prediction:
#         del(request.session["prediction"])
#     if request.method == "POST":
#         tempfile = request.FILES.get("file")

#         file = fs.save(tempfile.name, tempfile)
#         fileUrl = fs.url(file)

#         print("file is", file)

#         while not os.path.exists(os.path.join("media", file)):
#             time.sleep(1)
#         prediction = make_predictions(os.path.join("media", file))
#         print("this is the prediciton", prediction)
#         request.session["prediction"] = prediction
#         return redirect("home")

#     return render(request, "home.html", {"prediction": prediction})
