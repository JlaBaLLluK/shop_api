from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profile_settings.serializers import *
from rest_framework.status import *


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user_object = request.user
        if not check_password(serializer.data.get('old_password'), user_object.password):
            return Response({"errors": "Old password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        if serializer.data.get('new_password') != serializer.data.get('new_password_confirm'):
            return Response({"errors": "Failed to confirm new password!"}, status=HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('new_password'))
        except ValidationError as error:
            return Response({'errors': error.messages}, status=HTTP_400_BAD_REQUEST)

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

        user_object = request.user
        new_username = serializer.data.get('new_username')
        if user_object.username == new_username:
            return Response({"errors": "New username can't be the same as the old username!"},
                            status=HTTP_400_BAD_REQUEST)

        if new_username.count(' ') != 0:
            return Response({"errors": "Username can't contain spaces!"}, status=HTTP_400_BAD_REQUEST)

        if not check_password(serializer.data.get('password'), user_object.password):
            return Response({"errors": "This password is wrong!"}, status=HTTP_400_BAD_REQUEST)

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

        user_object = request.user
        if not check_password(serializer.data.get('password'), user_object.password) or not check_password(
                serializer.data.get('password_confirm'), user_object.password):
            return Response({"errors": "Failed to confirm password!"}, status=HTTP_400_BAD_REQUEST)

        user_object.delete()
        return Response({"success": "Account was deleted successfully!"}, status=HTTP_200_OK)


class ChangeOtherInformationView(APIView):
    serializer_class = ChangeOtherInformationInformationSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        serializer = ChangeOtherInformationInformationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        new_first_name = serializer.data.get('new_first_name')
        if new_first_name.count(' ') != 0 or (new_first_name != '' and not new_first_name.isalpha()):
            return Response({"errors": "New first name is invalid!"}, status=HTTP_400_BAD_REQUEST)

        new_last_name = serializer.data.get('new_last_name')
        if new_last_name.count(' ') != 0 or (new_last_name != '' and not new_last_name.isalpha()):
            return Response({"errors": "New last name is invalid!"}, status=HTTP_400_BAD_REQUEST)

        password = serializer.data.get('password')
        user_object = request.user
        if not check_password(password, user_object.password):
            return Response({"errors": "This password is wrong!"}, status=HTTP_400_BAD_REQUEST)

        serializer.update(user_object, serializer.validated_data)
        return Response({"success": "Data was changed successful!"}, status=HTTP_200_OK)
