import random
from rest_framework.views import APIView
from smtplib import SMTPException
from .serializers import ClientSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response


class RegisterView(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            email = user_data['email']
            code = random.randint(10000, 99999)
            # запись данных в Redis
            cache.set(f'verification_code_{email}', code, timeout=3600)
            cache.set(f'user_data_{email}', user_data, timeout=3600)

            # Отправка кода на почту
            try:
                send_mail(
                    'TaxiUNN Verification Code',
                    f'Your verification code is {code}',
                    'taxi.unn@mail.ru',
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Check your email for the verification code.'},
                                status=status.HTTP_200_OK)
            except SMTPException:
                return Response({'error': 'The email not found.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
