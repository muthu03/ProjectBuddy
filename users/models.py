from cProfile import Profile
from distutils.command.upload import upload
from email.policy import default
from operator import mod
from re import T
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


# Create your models here.
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    #have one to one relationship with 
    #if wemodify user model then there will be usses i authentication
    #So we create seperate profile model and then integrate it to the user inbuilt model
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.CharField(max_length=500,null=True,blank=True)
    username=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)

    short_intro=models.CharField(max_length=200,blank=True,null=True)
    bio=models.TextField(null=True,blank=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user-default.png')
    social_github=models.CharField(max_length=200,null=True,blank=True)
    social_twitter=models.CharField(max_length=200,null=True,blank=True)
    social_linkedin=models.CharField(max_length=200,null=True,blank=True)
    social_youtube=models.CharField(max_length=200,null=True,blank=True)
    social_website=models.CharField(max_length=200,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.username)

class skill(models.Model):
    owner=models.ForeignKey(profile,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.name)

class Messages(models.Model):
    #on delete the account the reciver will able to see the message and it should not be deleted
    sender=models.ForeignKey(profile,on_delete=models.SET_NULL,null=True,blank=True)
    #null = true means user dont have account can send message 
    recipient=models.ForeignKey(profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="messagess")
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.CharField(max_length=500,null=True,blank=True)
    subject=models.CharField(max_length=200,null=True,blank=True)
    body=models.TextField()
    is_read=models.BooleanField(default=False,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.subject)
    
    #when user open inbox it should order based on
    class Meta:
        ordering=['is_read','-created']
    





