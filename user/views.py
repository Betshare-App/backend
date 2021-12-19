from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserBalance, UserContact, UserDocs

# Create your views here.

class Register(APIView):
    permission_classes = [AllowAny,]
    @parser_classes([JSONParser])
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

class GetBalance(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_balance = UserBalance.objects.get(user=user)
            balance = user_balance.balance
            return Response(balance, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RegisterPersonalInfo(APIView):

    def get(self, request):
        data = request.data
        try:
            user = User.objects.get(id = request.user.id)
            first_name = user.first_name
            last_name = user.last_name
            docs = UserDocs.objects.get(user = user)
            rg = docs.RG
            cpf = docs.CPF
            date_of_birth = docs.date_of_birth
            contact = UserContact.objects.get(user = user)
            phone = contact.phone
            form = {"first_name": first_name,
                    "last_name": last_name,
                    "rg": rg,
                    "cpf": cpf,
                    "date_of_birth": date_of_birth,
                    "phone": phone}
            return Response(form, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(id=request.user.id)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            docs = UserDocs.objects.create(
                user=user, 
                RG=data['rg'], 
                date_of_birth=data['date_of_birth'],
                CPF=data['cpf'])
            
            contact = UserContact.objects.create(
                user=user, 
                phone=data['phone'])
            user.save()
            contact.save()
            docs.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
