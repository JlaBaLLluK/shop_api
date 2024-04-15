from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer


class VerificationCodeSerializer(Serializer):
    verification_code = IntegerField()
