
from django.contrib.auth.admin import User
from rest_framework import generics  
from rest_framework.permissions import AllowAny, IsAuthenticated

from automator.api.auth.serializer import GetUserSerializer, RegisterSerializer 


class RegiserUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes=[AllowAny]
    serializer_class=RegisterSerializer

class GetUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=GetUserSerializer

    def get_object(self):
        return self.request.user


