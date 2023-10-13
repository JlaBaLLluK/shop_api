from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from authorization.serializers import *


class LoginView(APIView):
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)

        user_object = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
        if user_object is None:
            return Response({"error": "Wrong credentials!"}, status=HTTP_401_UNAUTHORIZED)

        login(request, user_object)
        return Response({"success": "Login successful!"}, status=HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)
        return Response({"success": "Logout successful!"}, status=HTTP_200_OK)
