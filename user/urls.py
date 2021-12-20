from django.urls import path
from .views import (
    CheckCreditals, 
    GetBalance, 
    Register,
    RegisterAddressInfo,
    RegisterPersonalInfo)

urlpatterns = [
    path('register/', Register.as_view()),
    path('checkcredentials/', CheckCreditals.as_view()),
    path('getbalance/', GetBalance.as_view()),
    path('register/personal/', RegisterPersonalInfo.as_view()),
    path('register/address/', RegisterAddressInfo.as_view()),
]
