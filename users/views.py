from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from email import message
import imp
from multiprocessing import context
from operator import imod
from pydoc import describe
from django.contrib.auth.models import User

from django.shortcuts import render,redirect
from .models import profile
from django.contrib.auth import login,authenticate,logout

#to restrict un authenticated users to see add project page
from django.contrib.auth.decorators import login_required

#for flash messages
from django.contrib import messages

from .forms import CustomUserCreationForm,ProfileForm

def profiles(request):
    profiles=profile.objects.all()
    context={'profiles':profiles}
    return render(request,'users/profiles.html',context)
# Create your views here.

def loginUser(request):
    page='register'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method=="POST":
        #print(request.POST) when we click enter i.e login it print  password username and session ID
        username=request.POST['username']
        password=request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username Does Not Exsist')
            #authenticate will take username and password if password mathces then it will return user instance or null
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            #it will create session for the user and database 
            return redirect('profiles')
        else:
            messages.error(request,"username or password is incorrect")
    

    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User Successfully Loged Out')
    return redirect('login')

#user Registration
def registerUser(request):
    page='register'
    form=CustomUserCreationForm()

    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            #get the object before processing
            user.username=user.username.lower()
            user.save()

            messages.success(request,"User account was created")
            login(request,user)
            return redirect('edit-account')
        else:
            messages.success(request,"An Error Had Been Ocuured During the registration")



    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def userProfile(request,pk):
    profiless=profile.objects.get(id=pk)
    #they will have decription
    topSkills=profiless.skill_set.exclude(description__exact="")
    #they dont have description
    otherSkills=profiless.skill_set.filter(description="")
    context={
        'profile':profiless,
        'topSkills':topSkills,
        'otherSkills':otherSkills,
    } 
    return render(request,'users/user-profile.html',context)
@login_required(login_url='login')
def userAccount(request):
    #this will get the profile of loginned i nuser
    profile=request.user.profile
    skills=profile.skill_set.all()   
    projects=profile.project_set.all()
    context={'profile':profile,'skills':skills,'projects':projects,
    }
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.profile

    form=ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)#to process the file i.e image
        if form.is_valid():
            form.save()

            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)
