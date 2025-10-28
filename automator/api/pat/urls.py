

from os import name
from django.urls import path

from automator.api.pat.views import PATListCreateView, PATUpdateDeleteView


urlpatterns = [
    path('', PATListCreateView.as_view(), name='list_and_create_pat'),
    path("<pk>/", PATUpdateDeleteView.as_view(), name='update_or_delete_pat')
]