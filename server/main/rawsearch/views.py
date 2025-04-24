from ..models import Rxnconso
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
    
class SearchItemView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT str, rxaui, sab, rxcui FROM rxnconso WHERE rxcui LIKE %s",
            [query]
        )
        
        # Convert returned rows into a dictionary
        columns = [col[0] for col in cursor.description]
        return Response([dict(zip(columns, row)) for row in cursor.fetchall()])