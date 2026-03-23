from rest_framework import viewsets, permissions, status
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils import timezone
import random
from .models import User, OTPVerification
from .serializers import UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            # Handle password change directly if provided in the data
            if 'password' in request.data and request.data['password']:
                pwd = request.data['password']
                if len(pwd) < 8 or not re.search(r'[A-Z]', pwd) or not re.search(r'[a-z]', pwd) or not re.search(r'[^A-Za-z0-9]', pwd):
                    return Response({'detail': 'Password must be at least 8 characters long and contain uppercase, lowercase, and special characters.'}, status=status.HTTP_400_BAD_REQUEST)
                request.user.set_password(pwd)
            
            serializer.save()
            return Response(serializer.data)
            
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            code = f"{random.randint(100000, 999999)}"
            OTPVerification.objects.update_or_create(
                user=user,
                defaults={'code': code, 'created_at': timezone.now()}
            )
            
            send_mail(
                subject='Dashboard Verification Code',
                message=f'Your single-use 2FA verification code is: {code}',
                from_email='noreply@adc-consortium.org',
                recipient_list=[user.email],
                fail_silently=True,
            )
            
            return Response({'requires_2fa': True, 'username': username})
        return Response({'detail': 'No active account found with the given credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('otp')

        try:
            user = User.objects.get(username=username)
            otp_record = OTPVerification.objects.get(user=user)
            
            if otp_record.code == code and otp_record.is_valid():
                otp_record.delete()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            pass
            
        return Response({'detail': 'Invalid or expired OTP code'}, status=status.HTTP_400_BAD_REQUEST)
