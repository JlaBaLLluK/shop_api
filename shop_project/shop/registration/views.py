from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from registration.serializers import *
from user.models import AuthUser


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    @staticmethod
    def post(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = AuthUser.objects.create_user(username=request.data.get('username'),
                                            password=request.data.get('password'),
                                            email=request.data.get('email'),
                                            first_name=request.data.get('first_name'),
                                            last_name=request.data.get('last_name'),
                                            )
        return Response(UserRegistrationSerializer(user).data, status=HTTP_201_CREATED)
