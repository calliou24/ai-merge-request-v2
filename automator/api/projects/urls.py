

from django.urls import path

from automator.api.projects.views import DeleteProjectView, GetProjectBranches, GetProjectsView, SearchGitlabProjectView


urlpatterns=[ 
    path("", GetProjectsView.as_view() ,name='get_user_projects'),
    path("<pk>/delete/", DeleteProjectView.as_view(), name='delete_user_project'),
    path("<pk>/branches/", GetProjectBranches.as_view(), name='get_project_branches'),
    path('search/', SearchGitlabProjectView.as_view(), name='search_gl_project')
]