from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from user.models import AuthUser

user_model = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = user_model
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def save(self, **kwargs):
        user = AuthUser.objects.create_user(username=self.data['username'],
                                            password=self.data['password'],
                                            email=self.data['email'],
                                            first_name=self.data['first_name'],
                                            last_name=self.data['last_name'],
                                            is_active=False
                                            )
        return user


class UserRegistrationVerificationSerializer(Serializer):
    code = CharField(required=True, min_length=6, max_length=6)
