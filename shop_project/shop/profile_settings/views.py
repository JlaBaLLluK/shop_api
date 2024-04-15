from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profile_settings.serializers import *
from rest_framework.status import *

from user.serializers import UserSerializer


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = request.user
        if not check_password(serializer.data.get('password'), user_object.password):
            return Response({"errors": "Old password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        if serializer.data.get('new_password') != serializer.data.get('new_password_confirm'):
            return Response({"errors": "Failed to confirm new password!"}, status=HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('new_password'))
        except ValidationError as error:
            return Response({'errors': error.messages}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Password was changed successfully!"})


class ChangeUsernameView(APIView):
    serializer_class = ChangeUsernameSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangeUsernameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = request.user
        new_username = serializer.data.get('new_username')
        if user_object.username == new_username:
            return Response({"errors": "New username can't be the same as the old username!"},
                            status=HTTP_400_BAD_REQUEST)

        if not check_password(serializer.data.get('password'), user_object.password):
            return Response({"errors": "This password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Username was changed successfully!"})


class DeleteProfileView(APIView):
    serializer_class = DeleteProfileSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = DeleteProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = request.user
        if not check_password(serializer.data.get('password'), user_object.password) or not check_password(
                serializer.data.get('password_confirm'), user_object.password):
            return Response({"errors": "Failed to confirm password!"}, status=HTTP_400_BAD_REQUEST)

        user_object.delete()
        return Response({"success": "Account was deleted successfully!"})


class ChangeFirstLastNameView(APIView):
    serializer_class = ChangeFirstLastNameSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangeFirstLastNameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        password = serializer.data.get('password')
        user_object = request.user
        if not check_password(password, user_object.password):
            return Response({"errors": "This password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Data was changed successful!"})


class ChangeEmailView(APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangeEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = request.user
        serializer.update(user_object, serializer.validated_data)
        return Response(UserSerializer(request.user).data)
