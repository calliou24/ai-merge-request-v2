

from django.urls import path

from automator.api.auth.views import GetUserView, RegiserUserView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('me/', GetUserView.as_view(), name='get_user'),
    path('register/', RegiserUserView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(), name='user_login')
]