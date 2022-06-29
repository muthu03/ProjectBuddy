from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import projectForm

#to restrict un authenticated users to see add project page
from django.contrib.auth.decorators import login_required

# Create your views here.

def projects(request):
    projects=Project.objects.all()
    context={'projects':projects}
    return render(request,'projects/projects.html',context)
    
def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    tags=projectObj.tags.all()

    return render(request,'projects/single-project.html',{'project':projectObj,'tags':tags})

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