from rest_framework.views import APIView
from account.models import Profile
from django.http import request
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer,ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status


# Register API
@api_view(['POST'], )
def registerAPI(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data['response'] = 'succesfully registered'
        data['phone_number'] = account.phone_number
        data['username'] = account.username
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data)
    # serializer_class = RegisterSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #   
    #     return Response({
    #     "user": UserSerializer(user, context=self.get_serializer_context()).data,
    #     # "token": AuthToken.objects.create(user)[1]
    #     })
class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        profile = Profile.objects.get(id=self.request.user.id)