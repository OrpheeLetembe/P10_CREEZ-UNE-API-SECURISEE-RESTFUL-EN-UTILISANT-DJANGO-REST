from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import SignupSerializer


class SignupViewset(ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
