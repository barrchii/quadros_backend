import random
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from cart.models import CartItem


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

    # Migrate any guest cart items to this user
    session_key = request.session.session_key
    if session_key:
        CartItem.objects.filter(session_key=session_key).update(
            user=user, session_key=None
        )

    request.session['user_id'] = user.id
    request.session['user_email'] = user.email
    request.session.save()

    return Response({
        'message': 'Login successful',
        'user': {'email': user.email}
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def check_auth(request):
    user_email = request.session.get('user_email')
    if user_email:
        return Response({
            'authenticated': True,
            'email': user_email
        }, status=status.HTTP_200_OK)
    return Response({'authenticated': False}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def logout_view(request):
    request.session.flush()
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def delete_account(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'Not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    
    from .models import User
    try:
        user = User.objects.get(id=user_id)
        user.delete()
    except User.DoesNotExist:
        pass
    
    request.session.flush()
    return Response({'message': 'Account deleted'}, status=status.HTTP_200_OK)