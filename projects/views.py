from importlib.machinery import PathFinder
from operator import imod
from turtle import right, title
from unittest import result
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages

from .models import Project,Tag
from .forms import projectForm,ReviewForm
from django.db.models import Q

#to restrict un authenticated users to see add project page
from django.contrib.auth.decorators import login_required

from .utils import searchProjects,paginateProjects
# Create your views here.
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def projects(request):
    projects,search_query=searchProjects(request)
    custom_range,projects=paginateProjects(request,projects,3)


    context={'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)
    
def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    tags=projectObj.tags.all()
    form=ReviewForm()

    if request.method == 'POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=projectObj
        review.owner=request.user.profile
        review.save()
        projectObj.getVoteCount
        #calculate vote total and vote ratio by calling the functionin the models 
        messages.success(request,"your review was successfully submitted")
        return redirect('project',pk=projectObj.id)
        #we have to set user to review so we are making it as commit as false

        #update project vote count


    return render(request,'projects/single-project.html',{'project':projectObj,'tags':tags,'form':form})

#required user to be loged in
#and it will send user to login page
@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form=projectForm()

    if request.method=='POST':
        form=projectForm(request.POST,request.FILES)
        if form.is_valid():
            #if the form is POST operation and django check if the forms is valid 
            # and it will redirect ot projects page
            # and we save the model
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            
            return redirect('account')

    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile=request.user.profile

    project=profile.project_set.get(id=pk)
    form=projectForm(instance=project)
    #based on the click in the form EDIT , we will get project ID
    #Based on the project ID we get form for that project


    if request.method=='POST':
        form=projectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            #if the form is POST operation and django check if the forms is valid 
            # and it will redirect ot projects page
            # and we save the model
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile=request.user.profile

    #It will fisrt get ID of the project that has ot be deleted
    #Then it goes to the method and if the method is post i.e by clicking submit
    #it deleted the data and renders back to projects page
    project=profile.project_set.get(id=pk)
    context={'object':project}

    if request.method=='POST':
        project.delete()
        return redirect('account') 
 
     
    return render(request,'delete.html',context)