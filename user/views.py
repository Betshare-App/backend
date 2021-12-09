from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.

@parser_classes([JSONParser])
class Login(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if(user is not None):
            login(request, user)
            token = Token.objects.get(user__username=username)
            return Response(data={"token":token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

@parser_classes([JSONParser])
class Register(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        data = request.data
        try:
            if(User.objects.get(username=data['username'])):
                return Response({"message":"username já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
            elif(User.objects.get(username=data['email'])):
                return Response({"message":"email já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.save()
        return Response(data={"user":user.username},status=status.HTTP_201_CREATED)


class getUser(APIView):
    def get(self, request):
        data = request.data
        print(data['token'])
        try:
            user = User.objects.get(auth_token__key = data['token'])
            return Response({'user':str(user)}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CheckCreditals(APIView):
    permission_classes = [AllowAny,]
    @parser_classes([JSONParser,])
    def put(self, request):
        data =  request.data
        username =  data['username']
        email = data['email']
        username_isvalid = False
        email_isvalid = False
        try:
            user = User.objects.get(username=username)
        except:
            username_isvalid = True
        try:
            user = User.objects.get(email=email)
        except:
            email_isvalid = True
        return Response({'username_isvalid': username_isvalid, 'email_isvalid': email_isvalid})
