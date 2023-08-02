from account.models import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer,ProfileSerializer, AgentSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from agents.models import Agent
from rest_framework.authtoken.views import obtain_auth_token
from account.models import Account
from account.models import Account, Otp
from django.core.mail import send_mail


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
class UserProfileUpdateView(APIView):
    def get(self, request, format=None):
        profile = Profile.objects.get(user=self.request.user)
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
    def update(self,request, format=None):
        profile = Profile.objects.get(user=self.request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        return Response(serializer.data)
@api_view(['GET', 'PUT'], )
def profile(request):
    tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
    us = Token.objects.get(key=tkn).user
    profile = Profile.objects.get(user=us)
    usnm = us.phone_number
    if request.method == "PUT":
        d = request.data
        address = d['address']
        username= d['username']
        email = d['email']
        acc = Account.objects.filter(phone_number=usnm)
        prf_up = Profile.objects.filter(phone_number=usnm)
        if address is not '':
            acc.update(address=address)
            prf_up.update(address=address)
        if username is not '':
            acc.update(username=username)
            prf_up.update(username=username)
        if email is not '':
            acc.update(email=email)
            prf_up.update(email=email)
        
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)
class AgentView(APIView):
    def get(self, request, format=None):
        agent = Agent.objects.all()
        serializer = AgentSerializer(agent, many=True)
        return Response(serializer.data)
        

@api_view(["POST"])
def forget_pass_prep(request, *args, **kwargs):
    data = request.data
    email = data["email"]
    if Account.objects.filter(email=email).exists():
        usr = Account.objects.get(email=email)
        otp_creation = Otp.objects.create(user=usr)
        otp_creation.save()
        otp = Otp.objects.get(user=usr).otp
        send_mail(
            "azabazar forget password otp",
            f"The 6 digit otp is {otp}",
            'azabazar@azabazar.com',
            [email,],
            fail_silently=False
        )
        return Response(data={"otp": "otp send to mail"})
    return Response(data={"bad":"email didnot match"})


@api_view(["POST"])
def forget_pass_otp(request, *args, **kwargs):
    data = request.data
    usr = Account.objects.get(email=data["email"])
    user_otp = Otp.objects.get(user=usr).otp
    if str(data["otp"]) == str(user_otp):
        token = Token.objects.get(user=usr).key
        return Response(data={"Token": f"{token}"})
    else:
        return Response(status=404)

@api_view(["POST"])
def forget_pass(request, *args, **kwargs):
    tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
    us = Token.objects.get(key=tkn).user
    data = request.data
    if data["password"] == data["confirm_password"]:
        acc = Account.objects.get(phone_number=us.phone_number)
        acc.set_password(data["password"])
        acc.save()
    return Response(data={"success": "password changes successfully"})