from ..models import Rxnconso
from .serializers import SearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
    
class SearchItemView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        items = Rxnconso.objects.filter(rxcui=query)
        serializer = SearchSerializer(items, many=True)
        return Response(serializer.data)