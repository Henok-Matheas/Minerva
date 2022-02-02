from django.db import models
from django.contrib.auth.models import AbstractUser   


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
    school = models.ForeignKey(School, on_delete = models.CASCADE,null=True)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (str(self.name))

SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
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
     school = models.ForeignKey(School, on_delete = models.SET_NULL ,null = True)
     year = models.ForeignKey(Year, on_delete = models.SET_NULL ,null = True)
     semester  = models.ForeignKey(Semester, on_delete = models.SET_NULL ,null = True)

     USERNAME_FIELD = "username"
     REQUIRED_FIELDS = []  # Email & Password are required by default.

     def __str__(self):
        return self.first_name + self.last_name




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
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null=False)
    object = models.FileField(null = True)
    link = models.URLField(null = True)
    type = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null= False)
    description=models.TextField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return (self.name)



class Review(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE, null=False)
    material = models.ForeignKey(Material, on_delete = models.CASCADE, null=True)
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.review