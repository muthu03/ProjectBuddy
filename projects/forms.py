from dataclasses import fields
import imp
from tkinter.ttk import Widget
from django.forms import ModelForm
from .models import Project,Review
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


class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['value','body']

        labels={
        'value':'Place your Vote',
        'body':'Add your comment'
        }
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})