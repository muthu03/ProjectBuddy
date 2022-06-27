from django.contrib import admin

# Register your models here.
from .models import profile,skill
admin.site.register(profile)
admin.site.register(skill)