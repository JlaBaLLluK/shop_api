from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from registration.serializers import *
import random


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    @staticmethod
    def post(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('password'))
        except ValidationError as error:
            return Response({'error': error.messages}, status=HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response({'id': user.id, **serializer.data}, status=HTTP_201_CREATED)
    