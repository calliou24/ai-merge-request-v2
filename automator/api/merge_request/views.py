
import json
from gitlab import Gitlab, GitlabCreateError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from merge_automator.services.ai_providers import get_ai_mr_data

from .serializer import CreateMRDataSerializer, CreateMergeRequestDataSerializer, MergeRequestDataResponseSerializer
from .utils.diffs_utils import Build_optimized_diffs, extract_section

from ...models import PAT, Project, Template, AiProvider, AiModel

class GenerateMergeRequestDataView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = CreateMRDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        
        ai_provider_id = serializer.validated_data.get('provider_id')

        try:
            ai_provider = AiProvider.objects.get(id=ai_provider_id)
        except AiProvider.DoesNotExist:
            return Response({"errors": f"Provider with id {ai_provider_id} does not exist"}, HTTP_400_BAD_REQUEST)

        ai_model_id = serializer.validated_data.get('model_id') 

        try:
            ai_model = AiModel.objects.get(id=ai_model_id)
        except AiModel.DoesNotExist:
            return Response({"errors": f"Model with id {ai_model_id} does not exist"}, HTTP_400_BAD_REQUEST)
    
        project_id = serializer.validated_data.get('project_id')
        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return Response({"errors": f"Project with id: {project_id} does not exist"}, HTTP_400_BAD_REQUEST)
        
        pat_id = serializer.validated_data.get('pat_id')
        try:
            pat = PAT.objects.get(id=pat_id, user=request.user)
        except PAT.DoesNotExist:
            return Response({"errors": f"Personal Access Token with id {pat_id} does not exist"}, HTTP_400_BAD_REQUEST)

        template_id = serializer.validated_data.get('template_id')

        try:
            template = Template.objects.get(id=template_id, user=request.user)
        except Template.DoesNotExist:
            return Response({"errors": f"Template with id {template_id} does not exist"}, HTTP_400_BAD_REQUEST)
        
        gl = Gitlab(
            'https://gitlab.com',
            private_token=pat.encrypted_pat
        )

        gl_project = gl.projects.get(
            id=project.project_id
        )

        target_branch = serializer.validated_data.get('target_branch')
        origin_branch = serializer.validated_data.get('origin_branch')

        compare_diffs = gl_project.repository_compare(target_branch, origin_branch)

        optimized_diffs = Build_optimized_diffs(compare=compare_diffs)
        
        ai_context = serializer.validated_data.get('ai_context')
        mr_data = get_ai_mr_data(
            diffs=json.dumps(optimized_diffs),
            template=template.content,
            title=template.title,
            user_context=ai_context,
            provider_type=ai_provider.name,
            model=ai_model.name
        )

        if not mr_data:
            return Response({"errors": "Error generating merge request data, contact support for more information"}, HTTP_500_INTERNAL_SERVER_ERROR)

        title = extract_section(mr_data, "[title:start]", "[title:end]") 
        description = extract_section(mr_data, "[description:start]", "[description:end]")

        serialize_response = MergeRequestDataResponseSerializer({
            "title": title,
            "description": description
        })

        return Response(serialize_response.data, HTTP_200_OK)


class CreteMergeRequestView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = CreateMergeRequestDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        project_id = serializer.validated_data.get('project_id')
        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return Response({"errors": f"Project with id: {project_id} does not exist"}, HTTP_400_BAD_REQUEST)
        
        pat_id = serializer.validated_data.get('pat_id')
        try:
            pat = PAT.objects.get(id=pat_id, user=request.user)
        except PAT.DoesNotExist:
            return Response({"errors": f"Personal Access Token with id {pat_id} does not exist"}, HTTP_400_BAD_REQUEST)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        origin_branch = serializer.validated_data.get('origin_branch')
        target_branch = serializer.validated_data.get('target_branch')

        gl = Gitlab(
            'https://gitlab.com',
            private_token=pat.encrypted_pat
        )

        gl_project = gl.projects.get(
            id=project.project_id
        )

        try:
            merge_request = gl_project.mergerequests.create({
                'source_branch': origin_branch,
                'target_branch': target_branch, 
                'title': title,
                'description': description,          
            })
        except GitlabCreateError as error:
            return Response({"error": f"Error creating the merge request {str(error)}"}, error.response_code)
        except Exception as error:
            return  Response({"error": f"Error creating the merge request {str(error)}"}, HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": f"Merge request created successfully {merge_request.get_id()}"}, HTTP_200_OK)