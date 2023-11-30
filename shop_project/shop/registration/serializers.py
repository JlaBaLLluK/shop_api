from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from user.models import AuthUser

user_model = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = user_model
        fields = '__all__'

    def save(self, **kwargs):
        user = AuthUser.objects.create_user(username=self.data['username'],
                                            password=self.data['password'],
                                            email=self.data['email'],
                                            first_name=self.data['first_name'],
                                            last_name=self.data['last_name'],
                                            )
