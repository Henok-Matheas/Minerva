from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
)
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
    school = models.ForeignKey(School,on_delete=SET_NULL,null=True)
    description=models.TextField()

    # description = models.TextField("this is the {name}'st year in the {school}")

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (str(self.name))




class Semester(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.models.CharField(
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



class Member(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    school = models.ForeignKey(School, null = False)
    year = models.ForeignKey(Year, null = False)
    semester  = models.ForeignKey(Semester, null = False)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def __str__(self):
        return self.first_name + self.last_name

class Course(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School ,null= False)
    year = models.ForeignKey(Year ,null= False)
    semester = models.ForeignKey(Semester ,null= False)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (self.name)



class Material(models.Model):
    """this contains details about the particular school in the AAiT campus."""
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=CASCADE, null=False)
    object = models.FileField(null = True)
    link = models.URLField(null = True)
    type = models.CharField(max_length=50)
    course = models.ForeignKey(Course, null= False)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (self.name)



class Review(models.Model):
    host = models.ForeignKey(User, on_delete=CASCADE, null=False)
    material = models.ForeignKey(Material, on_delete=CASCADE, null=True)
    rating = models.IntegerField()
    review = models.TextField()