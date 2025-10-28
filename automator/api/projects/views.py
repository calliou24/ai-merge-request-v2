from gitlab import Gitlab, exceptions
from rest_framework.generics import DestroyAPIView, ListAPIView 
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_404_NOT_FOUND,    
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from automator.api.projects.serializers import ProjectBranchesSerializer, ProjectSerializer, SearchGilabProjectSerializer
from automator.models import PAT, Project

class DeleteProjectView(DestroyAPIView):
    queryset=Project.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=ProjectSerializer

class GetProjectsView(ListAPIView):
    queryset=Project.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=ProjectSerializer
    # pagination_class=[]

class SearchGitlabProjectView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SearchGilabProjectSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        pat: PAT = request.user.pats.filter(id=serializer.validated_data.get('pat_id')).first()

        if not pat: 
            return Response({"error": "Personal Accesss Token not found"}, HTTP_404_NOT_FOUND)
        
        gl = Gitlab(
            'https://gitlab.com',
            private_token=pat.encrypted_pat
        )

        try:
            url = serializer.validated_data.get('url')
            repo_url = url.split("gitlab.com/")[1].strip('/')

            if not repo_url:
                return Response({"error": f"Invalid project url: {serializer.url}"}, HTTP_400_BAD_REQUEST) 
        except Exception:
            return Response({"error": f"Invalid project url {serializer.url}"}, HTTP_400_BAD_REQUEST) 
        
        try:
            gl_project = gl.projects.get(repo_url)
        except exceptions.GitlabAuthenticationError as e:
                return Response({"error": "Access denied"}, HTTP_401_UNAUTHORIZED)
        except exceptions.GitlabGetError as e:
            if e.response_code == 404:
               return Response({"error": "Project not found"}, HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": f"GitLab Error: {str(e)}"}, HTTP_500_INTERNAL_SERVER_ERROR)
        

        project, _=Project.objects.get_or_create(
            user=request.user,
            name=gl_project.name,
            project_id=gl_project.id
        )
        gl_project.branches.list()

        serializer_project = ProjectSerializer(project)

        return Response(serializer_project.data, HTTP_200_OK) 

class GetProjectBranches(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        pat_id = request.query_params.get('pat_id')       

        if not pat_id or pat_id == '':
            return Response({"error": "Personal Access Token id its required"}, HTTP_400_BAD_REQUEST)

        project = Project.objects.get(id=pk)

        if not project:
            return Response({"error": f"Project with id {pk} not found"}, HTTP_404_NOT_FOUND)
        
        try:
            pat = PAT.objects.get(id=pat_id)
        except PAT.DoesNotExist:
            return Response({"error": f"Personal Access Token with id {pat_id} does not exist"}, HTTP_404_NOT_FOUND)

        gl = Gitlab(
            'https://gitlab.com',
            private_token=pat.encrypted_pat
        )
       
        try:
            gl_project = gl.projects.get(id=project.project_id)
        except exceptions.GitlabAuthenticationError as e:
                return Response({"error": "Access denied"}, HTTP_401_UNAUTHORIZED)
        except exceptions.GitlabGetError as e:
            if e.response_code == 404:
               return Response({"error": "Project not found"}, HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": f"GitLab Error: {str(e)}"}, HTTP_500_INTERNAL_SERVER_ERROR)
        
        serialize_branches = ProjectBranchesSerializer({
            "project_id": project.id,
            "branches": [branch.name for branch in gl_project.branches.list()]
        })

        return Response(serialize_branches.data, HTTP_200_OK)