from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import CustomLoginSerializer, CustomRegisterSerializer, CustomUserSerializer
from allauth.account.views import PasswordChangeView as AllAuthPasswordChangeView


class CustomLoginView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({'token': user.auth_token.key})

class CustomPasswordChangeView(AllAuthPasswordChangeView):
    permission_classes = (IsAuthenticated,)
    success_url = '/password-change/success/'

class CustomRegisterView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(self.request)
            return Response({'detail': 'Successfully registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer