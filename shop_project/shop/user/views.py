from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from user.models import AuthUser
from user.serializers import *


class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        return Response(UserSerializer(AuthUser.objects.get(username=request.user)).data, status=HTTP_200_OK)
