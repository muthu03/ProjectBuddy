from dataclasses import field, fields

from django.test import tag
from rest_framework import serializers
from projects.models import Project,Tag,Review
from users.models import profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=profile
        fields='__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields='__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner=ProfileSerializer(many=False) #this will connect to the profileserialiser and it wiill return back object
    #project serialiser as owner attribute and many=false is because we have just one owner
    tags=TagSerializer(many=True)
    #we wnat multiple tags
    reviews=serializers.SerializerMethodField()
    #It can be used to add any sort of data to the serialized representation of your object.
    #this will add review 
    
    class Meta:
        model=Project
        fields='__all__'
    def get_reviews(self,obj):
        reviews=obj.review.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data 

