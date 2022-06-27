from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import profile

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

def deleteUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()

   


post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender=profile)
#if user is deleted automatically profile is deleted
#if profile is deleted so we wrote above code to dlete the deleted profile user 
