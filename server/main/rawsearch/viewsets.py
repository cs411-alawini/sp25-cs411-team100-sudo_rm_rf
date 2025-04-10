from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..models import Rxnconso

from .serializers import SearchSerializer


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Rxnconso.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [AllowAny]