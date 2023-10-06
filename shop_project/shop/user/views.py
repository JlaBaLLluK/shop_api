from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from user.serializers import *


class UserView(APIView):
    serializer_class = UserSerializer

    @staticmethod
    def get(request, username):
        if str(request.user) != str(username):
            return Response({"error": "forbidden"}, status=HTTP_403_FORBIDDEN)

        return Response(UserSerializer(user.objects.get(username=username)).data, status=HTTP_200_OK)
