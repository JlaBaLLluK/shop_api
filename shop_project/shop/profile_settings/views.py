from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profile_settings.serializers import *
from rest_framework.status import *

from user.models import AuthUser


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = AuthUser.objects.get(username=request.user)
        if not check_password(serializer.data.get('old_password'), user_object.password):
            return Response({"errors": "Old password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        if serializer.data.get('new_password') != serializer.data.get('new_password_confirm'):
            return Response({"errors": "Failed to confirm new password"}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Password was changed successfully!"}, status=HTTP_200_OK)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        pass


class ChangeUsernameView(APIView):
    serializer_class = ChangeUsernameSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangeUsernameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = AuthUser.objects.get(username=request.user)
        if user_object.username == serializer.data.get('new_username'):
            return Response({"errors": "New username can't be the same as the old username!"},
                            status=HTTP_400_BAD_REQUEST)

        if not check_password(serializer.data.get('password'), user_object.password) or not check_password(
                serializer.data.get('password_confirm'), user_object.password):
            return Response({"errors": "Failed to confirm password!"}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Username was changed successfully!"}, status=HTTP_200_OK)


class DeleteProfileView(APIView):
    serializer_class = DeleteProfileSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = DeleteProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        print(request.user)
        user_object = AuthUser.objects.get(username=request.user)
        if not check_password(serializer.data.get('password'), user_object.password) or not check_password(
                serializer.data.get('password_confirm'), user_object.password):
            return Response({"errors": "Failed to confirm password!"}, status=HTTP_400_BAD_REQUEST)

        user_object.delete()
        return Response({"success": "Account was deleted successfully!"}, status=HTTP_200_OK)
