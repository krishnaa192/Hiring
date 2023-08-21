from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Candidate)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Recruiter)
admin.site.register(Apply)
