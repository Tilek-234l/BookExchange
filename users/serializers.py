from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user:
        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg, code='authorization')
    else:
        msg = _('Unable to log in with provided credentials.')
        raise serializers.ValidationError(msg, code='authorization')
    return user

class CustomLoginSerializer(serializers.Serializer):
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate_user(username, password)
        data['user'] = user
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomRegisterSerializer(serializers.Serializer):
    def save(self, request):
        email = self.validated_data['email']
        password = self.validated_data['password']
        user = User.objects.create_user(email=email, password=password)
        return user

class TokenObtainPairSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD
    default_error_messages = {
        'no_active_account': 'No active account found with the given credentials'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(
            write_only=True,
            trim_whitespace=False
        )

    def validate(self, attrs):
        user = authenticate_user(attrs[self.username_field], attrs['password'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class CustomLogoutSerializer(serializers.Serializer):
    """
    Serializer for logging out the user.
    """
    pass
