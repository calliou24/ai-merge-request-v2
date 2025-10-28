from rest_framework.urls import path

from .views import GenerateMergeRequestDataView, CreteMergeRequestView
urlpatterns = [
    path("generate/", GenerateMergeRequestDataView.as_view(), name='generate_mr_data'),
    path("create/", CreteMergeRequestView.as_view(), name='create_mr')
]