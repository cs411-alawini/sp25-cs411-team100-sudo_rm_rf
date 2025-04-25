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

class TopDrugsByConditionCountView(APIView):
    """
    Fetches the top 15 drugs associated with the most distinct conditions.
    """
    def get(self, request):
        # Your provided SQL query
        query = """
        SELECT
            rc.STR AS drug_name,
            c.RXCUI,
            c.condition_count
        FROM (
            SELECT RXCUI1 AS RXCUI, COUNT(DISTINCT condition_concept_name) AS condition_count
            FROM interactions
            WHERE condition_concept_name IS NOT NULL AND condition_concept_name != ''
              AND RXCUI1 IS NOT NULL AND RXCUI1 != ''
            GROUP BY RXCUI1
            ORDER BY condition_count DESC
            LIMIT 15
        ) AS c
        LEFT JOIN (
            SELECT RXCUI, MIN(STR) AS STR
            FROM rxnconso
            WHERE LAT = 'ENG' AND STR IS NOT NULL AND STR != '' -- Added LAT = 'ENG' for consistency
            GROUP BY RXCUI
        ) rc ON c.RXCUI = rc.RXCUI;
        """
        # Note: Added LAT='ENG' to the subquery for rxnconso for consistency
        # with the previous query, assuming you want English names.
        # Remove it if not desired.

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                # Filter out results where drug_name might be null due to LEFT JOIN
                results = [res for res in results if res.get('drug_name')]
            return Response(results)
        except Exception as e:
            # Basic error handling
            return Response({"error": str(e)}, status=500)


class DrugInteractingPartnersView(APIView):
    """
    Fetches the top 15 drugs interacting most frequently with a given target RXCUI,
    using the user's original UNION query structure and index-based result access.
    """
    def get(self, request, target_rxcui):
        # User's original query structure, parameterized
        query = """
        (SELECT
            RXCUI2, -- No alias needed here now
            COUNT(*) AS interaction_count
        FROM Interactions
        WHERE RXCUI1 = %s -- Placeholder for target RXCUI
        GROUP BY RXCUI2)
        UNION
        (SELECT
            RXCUI1, -- No alias needed here now
            COUNT(*) AS interaction_count
        FROM Interactions
        WHERE RXCUI2 = %s -- Placeholder for target RXCUI
        GROUP BY RXCUI1)
        ORDER BY interaction_count DESC
        LIMIT 15;
        """

        try:
            results = []
            with connection.cursor() as cursor:
                # Pass the target_rxcui parameter twice for the WHERE clauses
                cursor.execute(query, [target_rxcui, target_rxcui])

                # Fetch rows and construct dictionary using indices
                for row in cursor.fetchall():
                    results.append({
                        "RXCUI2": row[0], # First column (RXCUI2 or RXCUI1)
                        "interaction_count": row[1]  # Second column (interaction_count)
                    })
            return Response(results)
        except Exception as e:
            # Log the exception for more details during development
            print(f"Error in DrugInteractingPartnersView: {e}")
            # Basic error handling
            return Response({"error": "An internal server error occurred."}, status=500)