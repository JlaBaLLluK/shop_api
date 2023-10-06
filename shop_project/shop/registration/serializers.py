from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

user_model = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = user_model
        fields = '__all__'
