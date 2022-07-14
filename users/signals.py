from email import message
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import profile
from django.core.mail import send_mail
from django.conf import settings
#decirators
#@receiver(post_save,sender=profile)
#to trigger the signals whether user is createrd or not 



#signals
def createProfile(sender,instance,created,**kwargs):
   print('profile saved')
   # print("instancei",instance)   instance will be muthu becasue username ismuhtu  
   # print("created",created)          if it is created newly it will be True
   if created:
    user=instance
    profilee=profile.objects.create(
        user=user,
        username=user.username,
        email=user.email,
        name=user.first_name
    )
    subject='Welcome to the ProjectBuddy'
    message='We are glad you are Here'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [profilee.email],
        fail_silently=False
    )

def deleteUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()

   
def updateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user
    #to know whether first instance
    #whatever changes is done in via the profiel edit , it will change user also
    if created == False:
        user.first_name=profile.name
        user.email=profile.email
        user.username=profile.username
        user.save()

post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender=profile)
#if user is deleted automatically profile is deleted
#if profile is deleted so we wrote above code to dlete the deleted profile user 
post_save.connect(updateUser,sender=profile)
