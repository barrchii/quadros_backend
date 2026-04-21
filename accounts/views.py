import random
from datetime import timedelta

from django.contrib.auth import login
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .models import User, LoginCode
from .serializers import SendCodeSerializer, VerifyCodeSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def send_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    code = str(random.randint(100000, 999999))

    LoginCode.objects.create(email=email, code=code)

    # TO DO: send email via AWS SES — for now just print to console
    print(f'\n=== LOGIN CODE for {email}: {code} ===\n')

    return Response({'message': 'Code sent'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_code(request):
    serializer = VerifyCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    code = serializer.validated_data['code']

    ten_minutes_ago = timezone.now() - timedelta(minutes=10)

    login_code = LoginCode.objects.filter(
        email=email,
        code=code,
        is_used=False,
        created_at__gte=ten_minutes_ago
    ).first()

    if not login_code:
        return Response(
            {'error': 'Invalid or expired code'},
            status=status.HTTP_400_BAD_REQUEST
        )

    login_code.is_used = True
    login_code.save()

    user, created = User.objects.get_or_create(email=email)
    login(request, user)

    return Response({
        'message': 'Login successful',
        'user': {'email': user.email}
    }, status=status.HTTP_200_OK)