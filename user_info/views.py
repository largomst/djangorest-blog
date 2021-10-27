from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


from user_info.serializers import UserRegisterSerializer
from user_info.permissions import IsSelfOrReadyOnly


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [
                IsAuthenticatedOrReadOnly, IsSelfOrReadyOnly]
        return super().get_permissions()
