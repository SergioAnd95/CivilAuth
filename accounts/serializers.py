from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserGroup

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    email_interloc = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_repeat', 'email_interloc')
    
    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password_repeat')
        if password1 != password2:
            raise serializers.ValidationError('passwords not equals')
        
        email = data.get('email')
        email_interloc = data.get('email_interloc')

        if email == email_interloc:
            raise serializers.ValidationError('emails must be difference')

        if isinstance(email, User):
            user = email
        else:
            user = None
        
        try:
            user_interloc = User.objects.get(email=email_interloc)
        except User.DoesNotExist:
            user_interloc = None
        
        if (user and user_interloc and user_interloc.user_group.id != user.user_group.id) or (not user and user_interloc):
            raise serializers.ValidationError('User with email %s now in chat with another user' % email_interloc)

        if (user and not user_interloc):
            raise serializers.ValidationError('User with email %s doesn\'t invited you' % email_interloc)
        if user_interloc:
            data['email_interloc'] = user_interloc
        return data

    def validate_email(self, val):
        try:
            user = User.objects.get(email=val)
        except User.DoesNotExist:
            user = None
        
        if user and user.status == User.REGISTERED:
            raise serializers.ValidationError('user with this email already exists.')
        
        elif user:
            return user

        return val
        

    def create(self, validated_data):
        password = validated_data.pop('password')

        user_email = validated_data.get('email')
        email_interloc = validated_data.get('email_interloc')
        if isinstance(user_email, User):
            user = user_email
            user.status = User.REGISTERED
            user.set_password(password)
            user.save()
        else:
            group = UserGroup.objects.create()
            user = User.objects.create(
                email=user_email,
                user_group=group
            )
            user.set_password(password)
            user.save()
        
        if not isinstance(email_interloc, User):
            user_interloc = User.objects.create(
                email=email_interloc,
                status=User.INVITED,
                user_group=user.user_group
            )
        return user


class RefreshPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, val):
        try:
            user = User.objects.get(email=val)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email doesn\'t exist')
        
        if user.status == User.INVITED:
            raise serializers.ValidationError('User with this email was invited, please go to registration')
        
        return val