from rest_framework.permissions import IsAuthenticated 
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.response import Response

from automator.models import PAT


from .serializer import PATSerializer

# Create your views here.

class PATListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pats = request.user.pats.all()
        serializer = PATSerializer(pats, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request):
        serializer = PATSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(serializer.data, HTTP_201_CREATED)

class PATUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request, pk):
        pat = PAT.objects.get(id=pk)

        if not pat: 
            return Response({"error": "Personal Access Token not found"}, HTTP_404_NOT_FOUND)       

        serializer = PATSerializer(pat, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, HTTP_200_OK)