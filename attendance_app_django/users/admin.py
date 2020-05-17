from django.contrib import admin
from .models import Profile, Student, Staff, Admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Admin)
