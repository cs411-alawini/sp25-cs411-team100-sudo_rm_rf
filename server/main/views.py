# main/views.py
from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

# Keep any existing views you might have

class TopInteractionsView(APIView):
    """
    Fetches the top 15 interactions based on average PRR.
    """
    def get(self, request):
        # Your provided SQL query
        query = """
        WITH eng_names AS (
            SELECT RXCUI, MIN(STR) AS STR
            FROM rxnconso
            WHERE LAT = 'ENG' AND STR IS NOT NULL AND STR != ''
            GROUP BY RXCUI
        )
        SELECT
            top.avg_prr,
            top.interaction_count,
            rc1.STR AS drug_1_name,
            rc2.STR AS drug_2_name
        FROM (
            SELECT
                RXCUI1, RXCUI2,
                AVG(CAST(PRR AS DECIMAL(10,4))) AS avg_prr,
                COUNT(*) AS interaction_count
            FROM interactions
            WHERE PRR IS NOT NULL AND PRR != '' AND PRR REGEXP '^[0-9]+(\.[0-9]+)?$' -- Added check for numeric format
            GROUP BY RXCUI1, RXCUI2
            HAVING interaction_count > 5
            ORDER BY avg_prr DESC
            LIMIT 15
        ) AS top
        LEFT JOIN eng_names rc1 ON top.RXCUI1 = rc1.RXCUI
        LEFT JOIN eng_names rc2 ON top.RXCUI2 = rc2.RXCUI;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return Response(results)
        except Exception as e:
            # Basic error handling
            return Response({"error": str(e)}, status=500)