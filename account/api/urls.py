from .views import registerAPI, UserProfileUpdateView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', registerAPI, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('profile/', UserProfileUpdateView.as_view()),
]