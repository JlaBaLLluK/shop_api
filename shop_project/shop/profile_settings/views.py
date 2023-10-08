from rest_framework.views import APIView
from profile_settings.serializers import *


class ChangePasswordView(APIView):
    serializer_class = ...

    @staticmethod
    def put(request, username):
        pass


class ChangeUsernameView(APIView):
    serializer_class = ...

    @staticmethod
    def put(request, username):
        pass


class DeleteProfiledView(APIView):
    serializer_class = ...

    @staticmethod
    def delete(request, username):
        pass
