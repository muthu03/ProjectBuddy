from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from email import message
from gettext import install
import imp
from multiprocessing import context
from operator import imod
from pydoc import describe
import re
from django.contrib.auth.models import User

from django.shortcuts import render,redirect
from .models import profile, skill,Messages
from django.contrib.auth import login,authenticate,logout

#to restrict un authenticated users to see add project page
from django.contrib.auth.decorators import login_required

#for flash messages
from django.contrib import messages

from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm


from .utils import searchProfiles,paginateProfiles
def profiles(request):
    profiles,search_query=searchProfiles(request)
    custom_range,profiles=paginateProfiles(request,profiles,3)
    context={'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)
# Create your views here.

def loginUser(request):
    page='register'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method=="POST":
        #print(request.POST) when we click enter i.e login it print  password username and session ID
        username=request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
    context={'profile':profile,'skills':skills,'projects':projects}
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

@login_required(login_url='login')
def createSkill(request):
    profile=request.user.profile
    form=SkillForm()
    if request.method == 'POST':
        form=SkillForm(request.POST)
        if form.is_valid:
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'skill was added successfully')
            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)

    if request.method == 'POST':
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request,'skill was Updated')

            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)

def deleteSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,'skill was Deleted Successfully')

        return redirect('account')
    context={'object':skill}
    return render(request,'delete.html',context)
    
@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    messageRequests=profile.messagess.all()
    unreadCount=messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile=request.user.profile
    message=profile.messagess.get(id=pk)
    if message.is_read == False:
        message.is_read=True
        message.save()
    
    context={'message':message}
    return render(request,'users/message.html',context)

def createMessage(request, pk):
    recipient = profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message-form.html', context)



