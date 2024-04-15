from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import Serializer, ModelSerializer

from user.models import AuthUser


class ChangePasswordSerializer(ModelSerializer):
    new_password = CharField(required=True)
    new_password_confirm = CharField(required=True)

    class Meta:
        model = AuthUser
        fields = ('password', 'new_password', 'new_password_confirm')

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()


class ChangeUsernameSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = AuthUser

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.save()


class DeleteProfileSerializer(Serializer):
    password = CharField(required=True)
    password_confirm = CharField(required=True)


class ChangeFirstLastNameSerializer(ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('first_name', 'last_name', 'password')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()


class ChangeEmailSerializer(ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('email',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.save()
