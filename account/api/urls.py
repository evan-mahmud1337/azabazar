from .views import registerAPI, UserProfileUpdateView, AgentView, profile, forget_pass_prep, forget_pass,forget_pass_otp
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', registerAPI, name='register'),
    path('login/', obtain_auth_token, name='login'),
    # path('profile/', UserProfileUpdateView.as_view()),
    path('agent/', AgentView.as_view(), name='agents'),
    path('profile', profile, name="profile"),
    path('forget_pass_email/', forget_pass_prep, name="forget_pass_email"),
    path('otp_varification/', forget_pass_otp, name="otp"),
    path('forget_pass/', forget_pass, name="forget_pass"),
]