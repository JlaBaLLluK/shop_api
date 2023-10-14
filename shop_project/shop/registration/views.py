from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from registration.serializers import *


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    @staticmethod
    def post(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username')
        if username.count(' ') != 0:
            return Response({"errors": "Username can't contain spaces!"}, status=HTTP_400_BAD_REQUEST)

        first_name = serializer.data.get('first_name')
        if first_name.count(' ') != 0 or (first_name != '' and not first_name.isalpha()):
            return Response({"errors": "First name can't contain spaces or non-letters!"}, status=HTTP_400_BAD_REQUEST)

        last_name = serializer.data.get('last_name')
        if last_name.count(' ') != 0 or (last_name != '' and not last_name.isalpha()):
            return Response({"errors": "Last name can't contain spaces or non-letters!"}, status=HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('password'))
        except ValidationError as error:
            return Response({'error': error.messages}, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
        login(request, user)
        return Response(serializer.data, status=HTTP_201_CREATED)
