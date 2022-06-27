from multiprocessing import context
from pydoc import describe
from django.shortcuts import render
from .models import profile

def profiles(request):
    profiles=profile.objects.all()
    context={'profiles':profiles}
    return render(request,'users/profiles.html',context)
# Create your views here.


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
