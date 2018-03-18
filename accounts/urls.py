from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from . import views


urlpatterns = [
    path('accounts/login/', obtain_jwt_token, name='api_login'),
    path('accounts/verify/', verify_jwt_token, name='api_verify'),
    path('accounts/register/', views.UserCreateAPIView.as_view(), name='api_register'),
    path('accounts/refresh_password/', views.UserRefreshPassword.as_view(), name='api_refresh_password')
]
