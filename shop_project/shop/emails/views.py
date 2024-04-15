from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
import random

from emails.serializers import VerificationCodeSerializer
from user.models import AuthUser


class SendVerificationCodeView(APIView):
    serializer_class = VerificationCodeSerializer
    verification_code = None

    @staticmethod
    def get(request, pk):
        VerificationCodeSerializer.verification_code = random.randint(100000, 999999)
        subject = "Confirm registration"
        message = (f"Your verification code is {VerificationCodeSerializer.verification_code}. "
                   f"Enter this code to finish your registration.")
        recipient_list = [AuthUser.objects.get(pk=pk).email]
        send_mail(subject, message, None, recipient_list)
        return Response({'info': 'Verification code was sent on your email!'})

    @staticmethod
    def post(request, pk):
        serializer = VerificationCodeSerializer(data=request.data)
        if (not serializer.is_valid() or
                serializer.data.get('verification_code') != VerificationCodeSerializer.verification_code):
            return Response({'error': 'This code is wrong!'}, status=HTTP_400_BAD_REQUEST)

        user = AuthUser.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return Response({'success': 'Account was verified successfully!'})
