from django.contrib.auth import login
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

        try:
            validate_password(request.data.get('password'))
        except ValidationError as error:
            return Response({'error': error.messages}, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
