from rest_framework import viewsets, status
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.settings import api_settings
from .models import User
from .permissions import IsActivePortalAdmin, IsActivePortalStaff
from .serializers import UserMeSerializer, UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsActivePortalStaff]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'me':
            return UserMeSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'me':
            return [IsActivePortalStaff()]
        return [IsActivePortalAdmin()]

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

class StaffTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        **TokenObtainPairSerializer.default_error_messages,
        'no_active_account': 'No active account found with the given credentials',
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active or self.user.role not in {'staff', 'admin'}:
            raise AuthenticationFailed(self.error_messages['no_active_account'])
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = StaffTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'staff_login'


class StaffTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            token = self.token_class(attrs['refresh'])
        except TokenError as error:
            raise InvalidToken(error.args[0]) from error
        user_id = token.get(api_settings.USER_ID_CLAIM)
        user = User.objects.filter(pk=user_id).first()
        if not user or not user.is_active or user.role not in {'staff', 'admin'}:
            raise InvalidToken('No active staff portal account found for this token')
        return super().validate(attrs)


class StaffTokenRefreshView(TokenRefreshView):
    serializer_class = StaffTokenRefreshSerializer
