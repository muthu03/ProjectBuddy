import imp
from tkinter.ttk import Widget
from django.forms import ModelForm
from .models import Project
from django import forms

class projectForm(ModelForm):
    class Meta:
        model=Project
        fields=['title','description','featured_image','demo_link','source_link','tags']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(projectForm,self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


        
