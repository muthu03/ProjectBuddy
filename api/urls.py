from django.urls import path
from .import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView, #see jwt documentation , it is to generate token based on the user , 
    #wehn we usubmit user and password

    TokenRefreshView,
)

urlpatterns=[
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #referesh token is gonna give token to generte new token it will timespan of 5 min and it will expires
    path('',views.getRoutes),
    path('projects/',views.getProjects),
    path('projects/<str:pk>',views.getProject)


]