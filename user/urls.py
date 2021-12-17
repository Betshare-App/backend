from django.urls import path
from .views import CheckCreditals, GetBalance, Register

urlpatterns = [
    path('register/', Register.as_view()),
    path('checkcredentials/', CheckCreditals.as_view()),
    path('getbalance/', GetBalance.as_view()),
]
