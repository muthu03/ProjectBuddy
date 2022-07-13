from cProfile import Profile
from email.policy import default
from enum import unique
from tkinter import CASCADE, FLAT
from django.db import models
import uuid
from users.models import profile

# Create your models here.
class Project(models.Model):
    owner=models.ForeignKey(profile,null=True,blank=True,on_delete=models.SET_NULL)
    title=models.CharField(max_length=200)
    #We created title wiht max char of 20
    description=models.TextField(null=True,blank=True)
    #description can be blank

    featured_image=models.ImageField(null=True,blank=True,default="default.jpg")
    demo_link=models.CharField(max_length=200,null=True,blank=True)
    source_link=models.CharField(max_length=200,null=True,blank=True)

    #gives relation
    tags=models.ManyToManyField('Tag',blank=True)
    
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)



    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title

    class Meta:
        #order the project by top voted  in descending order so -
        ordering=['-vote_ratio','-vote_total','title']
    
    @property 
    def reviewers(self):
        #this will give everyhting as list bcz flat =True and we are having list of ID s who are done wiht review
        queryset=self.review.all().values_list('owner__id',flat=True)
        return queryset




    @property
    def getVoteCount(self):
        reviews = self.review.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    #This is used for drop down list i.e to up vote and down vote
    VOTE_TYPE=[
        ('up','Up Vote'),
        ('down','Down Vite'),
    ]
    owner=models.ForeignKey(profile,on_delete=models.CASCADE,null=True)
    # if project is deleted all reviews will be deleted using cascade
    #To handle One-To-Many relationships in Django you need to use ForeignKey 
    #this access project model and that return project.title
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="review")
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.value
    
    #user can give only one review so we need to bind the both owner and project
    class Meta:
        unique_together=[['owner','project']] 
    
  




#mant to many relationship
class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name
