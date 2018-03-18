from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from .serializers import UserRegisterSerializer, RefreshPasswordSerializer
from .mailgun_utils import send_message
# Create your views here.

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permissions = [AllowAny, ]


class UserRefreshPassword(APIView):
        
    def post(self, request, *args, **kwargs):
        """
        Endpoint for refresh user password
        ---
        request_serializer: RefreshPasswordSerializer
        """
        serializer = RefreshPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.get(email=email)
        new_password = User.objects.make_random_password(length=8)
        msg = 'Your new password: %s' % new_password
        resp = send_message(
            settings.MAILGUN_DEFAULT_SENDER_EMAIL, 
            'New password', 
            msg, 
            [email, ]
        )
        if resp.status_code == 200:
            user.set_password(new_password)
            user.save()
            data = {'message': 'Message with new password was sent to your email %s' % email}
            status = 200
        else:
            data = {'email_error': 'Can\'t send email'}
            status = 400
        return Response(data, status=status)