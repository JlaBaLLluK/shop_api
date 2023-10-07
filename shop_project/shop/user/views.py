from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from user.models import AuthUser
from user.serializers import *


class UserView(APIView):
    serializer_class = UserSerializer

    @staticmethod
    def get(request, username):
        return Response(UserSerializer(AuthUser.objects.get(username=username)).data, status=HTTP_200_OK)
