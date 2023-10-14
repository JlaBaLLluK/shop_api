from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import Serializer


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)
    new_password_confirm = CharField(required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()


class ResetPasswordSerializer(Serializer):
    pass


class ChangeUsernameSerializer(Serializer):
    new_username = CharField(required=True)
    password = CharField(required=True)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('new_username')
        instance.save()


class DeleteProfileSerializer(Serializer):
    password = CharField(required=True)
    password_confirm = CharField(required=True)


class ChangeOtherInformationInformationSerializer(Serializer):
    new_email = EmailField(required=False, default='')
    new_first_name = CharField(required=False, default='')
    new_last_name = CharField(required=False, default='')
    password = CharField(required=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('new_first_name')
        instance.last_name = validated_data.get('new_last_name')
        instance.email = validated_data.get('new_email')
        instance.save()
