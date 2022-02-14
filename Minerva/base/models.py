import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError   

validUsername = "[A-Z][A-Z][A-Z]/[0-9][0-9][0-9][0-9]/[0-9][0-9]"

def validName(value):
    if not re.match(validUsername,value):
        raise ValidationError(str(value) + "Enter ValidUsername")

# Create your models here.
class School(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.CharField(max_length=50)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (self.name)

class Year(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.IntegerField()
    school = models.ManyToManyField(School)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (str(self.name))

SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("pre","pre-engineering"),
)

class Semester(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.CharField(
        max_length = 20,
        choices = SEMESTER_CHOICES,
        default = '1'
        )
    year= models.ManyToManyField(Year)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (str(self.name))

class User(AbstractUser):
     username = models.CharField(max_length= 11 ,validators= [validName], unique= True)
     school = models.ForeignKey(School, on_delete = models.SET_NULL ,null = True, default= None)
     year = models.ForeignKey(Year, on_delete = models.SET_NULL ,null = True, default= None)
     semester  = models.ForeignKey(Semester, on_delete = models.SET_NULL ,null = True, default= None)

     USERNAME_FIELD = "username"
     REQUIRED_FIELDS = []  # Email & Password are required by default.

     def __str__(self):
        return self.username

class Course(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School ,on_delete = models.CASCADE, null= False)
    year = models.ForeignKey(Year ,on_delete = models.CASCADE, null= False)
    semester = models.ForeignKey(Semester ,on_delete = models.CASCADE, null= False)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (self.name)



class Material(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    host = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length = 50)
    description=models.TextField()
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null= False)
    thumbnail = models.ImageField(null = True)
    file = models.FileField(upload_to = "files",null = True)
    type = models.CharField(max_length=50)
    count = models.IntegerField(null = True,default= 0)
    rating = models.DecimalField(decimal_places= 1, max_digits= 10, default= 0.0)

    def addRating(self,rating):
        self.rating += rating
    class Meta:
        ordering = ['-name']

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        self.file.delete()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return (self.name)

class Review(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE, null=False)
    material = models.ForeignKey(Material, on_delete = models.CASCADE, null=True, related_name='reviews')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.review