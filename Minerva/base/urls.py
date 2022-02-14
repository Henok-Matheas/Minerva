from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("",views.home, name = "home"),
     path("user/",views.user, name = "user"),
     path("login/", views.loginPage, name="login"),
     path("logout/", views.logoutUser, name="logout"),
     path("register/", views.registerPage, name="register"),
     path("upload/", views.upload, name="upload"),
     path("delete_file/<str:pk>", views.deleteFile, name="delete_file"),
     path("materials/<str:pk>", views.material, name="material") 
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)