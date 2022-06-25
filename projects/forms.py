from django.forms import ModelForm
from .models import Project


class projectForm(ModelForm):
    class Meta:
        model=Project
        fields=['title','description','featured_image','demo_link','source_link','tags']