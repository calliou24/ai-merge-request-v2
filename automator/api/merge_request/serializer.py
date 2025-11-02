
from rest_framework import serializers 

class CreateMRDataSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()
    model_id = serializers.IntegerField()

    project_id = serializers.IntegerField()
    template_id = serializers.IntegerField()
    pat_id = serializers.IntegerField()
    origin_branch = serializers.CharField()
    target_branch = serializers.CharField()
    ai_context = serializers.CharField()

class MergeRequestDataResponseSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1)
    description = serializers.CharField(min_length=1)

class CreateMergeRequestDataSerializer(serializers.Serializer):
    project_id=serializers.IntegerField()
    pat_id=serializers.IntegerField()

    #
    title=serializers.CharField()
    description=serializers.CharField()
    origin_branch = serializers.CharField()
    target_branch = serializers.CharField()
