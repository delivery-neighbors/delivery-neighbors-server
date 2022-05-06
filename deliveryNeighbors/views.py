from rest_framework.generics import *

from deliveryNeighbors.models import *
from deliveryNeighbors.serializers import *


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
