from cProfile import Profile
from email.policy import default
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
        #order the project by created date in ascending order
        ordering=['created']

class Review(models.Model):
    #This is used for drop down list i.e to up vote and down vote
    VOTE_TYPE=[
        ('up','Up Vote'),
        ('down','Down Vite'),
    ]
    #owner=
    # if project is deleted all reviews will be deleted using cascade
    #To handle One-To-Many relationships in Django you need to use ForeignKey 
    #this access project model and that return project.title
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.value

#mant to many relationship
class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name
