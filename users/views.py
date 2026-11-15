from rest_framework import viewsets, permissions, status
import re
from rest_framework.decorators import action
from .models import User
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
