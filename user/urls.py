from django.urls import path
from .views import (
    CheckCreditals,  
    Register,
    getUserData)

urlpatterns = [
    path('register/', Register.as_view()),
    path('checkcredentials/', CheckCreditals.as_view()),
    path('user/', getUserData.as_view()),
]
