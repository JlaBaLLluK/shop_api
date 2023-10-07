from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

user = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class ChangePasswordSerializer(Serializer):
    old_password = CharField()
    new_password = CharField()
    new_password_confirm = CharField()


class ChangeUsernameSerializer(Serializer):
    new_username = CharField()
    password = CharField()
    password_confirm = CharField()
