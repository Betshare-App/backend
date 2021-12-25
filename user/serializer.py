from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import UserAddress, UserDocs, UserFinanceInfo

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocs
        fields = '__all__'

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'

class UserFinanceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFinanceInfo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userdocs = UserDocsSerializer()
    useraddress = UserAddressSerializer()
    userfinanceinfo = UserFinanceInfoSerializer()
    class Meta:
        model = User
        fields = (
            'username', 
            'userdocs',  
            'useraddress',
            'userfinanceinfo',)
