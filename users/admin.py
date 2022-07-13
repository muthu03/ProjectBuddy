from django.contrib import admin

# Register your models here.
from .models import profile,skill,Messages
admin.site.register(profile)
admin.site.register(skill)
admin.site.register(Messages)