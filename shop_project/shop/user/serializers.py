from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

user = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
