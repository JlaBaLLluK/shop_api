from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from user.models import AuthUser
from user.serializers import *


class UserView(APIView):
    serializer_class = UserSerializer

    @staticmethod
    def get(request, username):
        if str(request.user) != str(username):
            return Response({"error": "Access denied!"}, status=HTTP_403_FORBIDDEN)

        return Response(UserSerializer(AuthUser.objects.get(username=username)).data, status=HTTP_200_OK)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer

    @staticmethod
    def get(request, username):
        if str(request.user) != str(username):
            return Response({"error": "Access denied!"}, status=HTTP_403_FORBIDDEN)

        return Response(status=HTTP_200_OK)

    @staticmethod
    def put(request, username):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")
        user_object = user.objects.get(username=username)
        if not check_password(old_password, user_object.password):
            return Response({"error": "Old password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirm:
            return Response({"error": "Passwords are different!"}, status=HTTP_400_BAD_REQUEST)

        validate_password(new_password)
        user_object.set_password(new_password)
        user_object.save()
        print(new_password)
        return Response({"success": "Password was changes successfully"}, status=HTTP_200_OK)


class ChangeUsernameView(APIView):
    serializer_class = ChangeUsernameSerializer

    @staticmethod
    def get(request, username):
        if str(request.user) != str(username):
            return Response({"error": "Access denied!"}, status=HTTP_403_FORBIDDEN)

        return Response(status=HTTP_200_OK)

    @staticmethod
    def put(request, username):
        if str(request.user) != str(username):
            return Response({"error": "Access denied!"}, status=HTTP_403_FORBIDDEN)

        new_username = request.data.get('new_username')
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')
        user_object = user.objects.get(username=username)
        if not check_password(password, user_object.password):
            return Response({"error": "Password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        if password != password_confirm:
            return Response({"error": "Passwords are different!"}, status=HTTP_400_BAD_REQUEST)

        user_object.username = new_username
        user_object.save()
        return Response({"success": "Username was changes successfully"}, status=HTTP_200_OK)


class DeleteProfileView(APIView):
    pass
