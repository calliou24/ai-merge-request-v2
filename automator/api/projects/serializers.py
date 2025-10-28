from rest_framework import serializers

from automator.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','name','project_id']

class SearchGilabProjectSerializer(serializers.Serializer):
    pat_id=serializers.IntegerField(required=True)
    url=serializers.CharField(required=True)

class GetProjectBranchesSerializer(serializers.Serializer):
    pat_id=serializers.IntegerField(required=True)



class ProjectBranchesSerializer(serializers.Serializer):
    project_id=serializers.IntegerField()
    branches=serializers.ListField()