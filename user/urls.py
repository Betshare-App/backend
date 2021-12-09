from django.urls import path
from .views import CheckCreditals, Login, Logout, Register, getUser
from rest_framework.authtoken import views

urlpatterns = [
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('register/', Register.as_view()),
    path('getuser/', getUser.as_view()),
    path('checkcredentials/', CheckCreditals.as_view()),
]

urlpatterns += [
    path('token-auth/', views.obtain_auth_token)
]