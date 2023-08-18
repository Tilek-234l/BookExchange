from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_auth.views import LogoutView as RestAuthLogoutView
from allauth.account.views import PasswordChangeView as AllAuthPasswordChangeView
from .serializers import CustomLoginSerializer, CustomRegisterSerializer, CustomLogoutSerializer
from django.shortcuts import render

class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer
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
    serializer_class = CustomRegisterSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(self.request)
            return Response({'detail': 'Успешно зарегистрировано'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLogoutView(RestAuthLogoutView):
    serializer_class = CustomLogoutSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
        return response
