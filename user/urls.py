from django.urls import path
from .views import CheckCreditals, GetBalance, Register
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', Register.as_view()),
    path('checkcredentials/', CheckCreditals.as_view()),
    path('getbalance/', GetBalance.as_view()),
]

urlpatterns += [
    path('token-auth/', views.obtain_auth_token)
]