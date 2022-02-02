from django.contrib import admin
from base.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(School)
admin.site.register(Year)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Review)