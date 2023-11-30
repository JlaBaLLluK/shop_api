from rest_framework.fields import CharField
from rest_framework.serializers import Serializer


class LoginSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)
