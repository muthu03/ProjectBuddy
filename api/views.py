from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

#tell us about all the url path
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'}, #reutne all projects
        {'GET':'/api/projects/id'}, #return single project
        {'POST':'/api/projects/id/vote'}, #this will help to vote on the project 

        {'POST':'api/users/token'},#this takes in   post request for login and it is already pre built routes in django and it generate token for user for login
        #this take post data to user/token
        {'POST':'api/users/token/refresh'},#this makes data to refresh and it will logged out after few minutes
    ]
    return Response(routes)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProjects(request):
    print('USER ',request.user)
    projects=Project.objects.all()
    #we nee JSON data so we are serialising
    serializer=ProjectSerializer(projects,many=True) #we will be getting many objects 
    return Response(serializer.data) # to get data out of class we need to use serialiser.data

@api_view(['GET'])
def getProject(request,pk):
    project=Project.objects.get(id=pk)
    serializer=ProjectSerializer(project,many=False) 
    return Response(serializer.data) 
