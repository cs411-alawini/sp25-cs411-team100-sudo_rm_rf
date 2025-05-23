# main/views.py
from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

from main.models import Users

# Keep any existing views you might have

class TopInteractionsView(APIView):
    """
    Fetches the top 15 interactions based on average PRR.
    """
    def get(self, request):
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
            return Response({"error": str(e)}, status=500)

class TopDrugsByConditionCountView(APIView):
    """
    Fetches the top 15 drugs associated with the most distinct conditions.
    """
    def get(self, request):
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
    
class UserRegistrationView(APIView):
    """
    Handles user registration.
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            with connection.cursor() as cursor:
                # Insert new user into the Users table
                cursor.execute(
                    "INSERT INTO Users (email, password_hash) VALUES (%s, %s)",
                    [email, password]
                )
                cursor.execute(
                    "SELECT user_id FROM users WHERE email = %s AND password_hash = %s",
                    [email, password]
                )

                user_id = cursor.fetchone()
            return Response({"email": email, "user_id": user_id}, status=201)
        except Exception as e:
            return Response({"error": "An error occurred during registration"}, status=500)
    
    def get(self, request):
        return Response({"message": "UserRegistrationView is working!"}, status=200)
    
    def delete(self, request):
        user_id = request.data.get('user_id')

        query = """
            START TRANSACTION;

            CREATE TABLE Deleted(
                id INT
            );

            INSERT INTO Deleted (SELECT result_id FROM Results WHERE user_id = %s);

            DELETE FROM Results WHERE user_id = %s;
            DELETE FROM junction WHERE result_id IN (SELECT id FROM Deleted);
            DELETE FROM Users WHERE user_id = %s;

            DROP TABLE Deleted;

            COMMIT;
        """

        try:
            # results = []
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id, user_id, user_id])

            return Response({"message": "Login successful", "user_id": user_id}, status=200)
        except:
            return Response({"error": "An error occurred during deletion"}, status=500)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # print(Users.objects.all())
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id, password_hash FROM Users WHERE email = %s", [email])
                row = cursor.fetchone()

                if row is None:
                    return Response({"error": "Invalid credentials"}, status=401)

                user_id, password_hash = row

                if password_hash == password:
                    return Response({"message": "Login successful", "user_id": user_id}, status=200)
                else:
                    return Response({"error": "Invalid credentials"}, status=401)         
        except:
            return Response({"error": "An error occurred during login"}, status=500)

class UserDrugs(APIView):
    def get(self, request):
        user_id = request.data.get("user_id")
        result_id = request.data.get("result_id")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                                SELECT DISTINCT interactions.rxcui1, interactions.rxcui2
                                FROM users JOIN results JOIN junction LEFT JOIN interactions ON junction.inter_id = interactions.inter_id
                                WHERE users.user_id = %s AND result_id = %s;
                                """,
                                [user_id, result_id])
                rows = cursor.fetchall()
            
            results = set()
            for row in rows:
                results.add(row[0], row[1])
            return Response({"result": list(results)}, status = 200)
        except Exception as e:
            return Response({"message": "Problem retrieving user medications"}, status = 500)
        

class AddMedication(APIView):
    def post(self, request):
        result_id = request.data.get("result_id")
        rxcui = request.data.get("rxcui")
        #print(result_id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT interactions.rxcui1 " \
                "FROM junction LEFT JOIN interactions ON junction.inter_id = interactions.inter_id WHERE junction.result_id = %s "
                "UNION "
                "SELECT DISTINCT interactions.rxcui2 "
                "FROM junction LEFT JOIN interactions ON junction.inter_id = interactions.inter_id WHERE junction.result_id = %s",
                [result_id, result_id]
            )
            rows = cursor.fetchall()

        print(rows)
        if len(rows) == 0: # User has no drugs for this result_id
            with connection.cursor() as cursor:
                
                cursor.execute("INSERT INTO junction (result_id, inter_id, rxcui1, rxcui2) " \
                "VALUES (%s, %s, %s, %s)", [result_id, "1", rxcui, rxcui])
                return Response(status = 200)
        
        elif len(rows) == 2 and rows[1][0] == "F00103": # User has one drug (and has inter_id of 1 as a placeholder)
            with connection.cursor() as cursor:
                # print(temp_inter_id)
                cursor.execute("SELECT rxcui1 FROM junction WHERE result_id = %s", [result_id])
                prev_rxcui = cursor.fetchone()
                # print(rxcui, prev_rxcui[0])

                cursor.execute("SELECT inter_id FROM interactions WHERE (rxcui1 = %s AND rxcui2 = %s) OR (rxcui1 = %s AND rxcui2 = %s)",
                [rxcui, prev_rxcui[0], prev_rxcui[0], rxcui])
                temp_inter_id = cursor.fetchone()

                cursor.execute("UPDATE junction SET rxcui2 = %s, inter_id = %s WHERE result_id = %s AND rxcui1 = %s",
                [rxcui, temp_inter_id[0], result_id, prev_rxcui])
                return Response(status = 200)
            
        else:
            all_rxcuis = set()
            for row in rows:
                all_rxcuis.add(row[0])
            with connection.cursor() as cursor:
                for exist_rxcui in all_rxcuis:
                    cursor.execute(
                        "SELECT DISTINCT inter_id FROM interactions WHERE (rxcui1 = %s AND rxcui2 = %s) OR (rxcui1 = %s AND rxcui2 = %s)",
                        [rxcui, exist_rxcui, exist_rxcui, rxcui]
                    )   
                    temp_inter_id = cursor.fetchone()
                    # print(temp_inter_id)
                    cursor.execute("INSERT INTO junction (result_id, inter_id, rxcui1, rxcui2) " \
                    "VALUES (%s, %s, %s, %s)", [result_id, temp_inter_id[0], rxcui, exist_rxcui])
            return Response(status = 200)
    
class DeleteMedication(APIView):
    def post(self, request):
        result_id = request.data.get("result_id")
        rxcui = request.data.get("rxcui")
        print(rxcui)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM junction WHERE result_id = %s AND (rxcui1 = %s OR rxcui2 = %s)",
                [result_id, rxcui, rxcui]
            )

        return Response(status = 200)
        """
            cursor.execute(
                "SELECT DISTINCT rxcui1 FROM junction LEFT JOIN interactions ON junction.inter_id = interactions.inter_id WHERE junction.result_id = %s",
                [result_id]
            )
            all_rxcuis = set()
            for row in cursor.fetchall():
                all_rxcuis.add(row[0])
             
        with connection.cursor() as cursor:
            for exist_rxcui in all_rxcuis:
                cursor.execute(
                    "SELECT DISTINCT inter_id FROM interactions WHERE (rxcui1 = %s AND rxcui2 = %s) OR (rxcui1 = %s AND rxcui2 = %s)",
                    [rxcui, exist_rxcui, exist_rxcui, rxcui]
                )   
                temp_inter_id = cursor.fetchone()
                print(temp_inter_id)
                cursor.execute("DELETE FROM junction WHERE result_id = %s AND inter_id = %s", [result_id, temp_inter_id[0]])
        return Response(status = 200)
        """
    
class GetResultIds(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        #print(user_id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT result_name, result_id FROM results WHERE user_id = %s", 
                [user_id]
            )
            temp_results = cursor.fetchall()
            #print(temp_results)
        formated_results = []
        for idx, res_id in enumerate(temp_results):
            formated_results.append({"id": res_id[1], "name": res_id[0]})
        #print(formated_results)
        return Response(formated_results, status = 200)

"""
# Seperate searchboxes for 
class GenericTextSearch(APIView):
    def get(self, request):
        search_string = request.query_params.get("search_string")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT rxcui1 FROM interactions WHERE drug_1_concept_name LIKE %s",
                [f"%{search_string}%"]
            )
            return Response(cursor.fetchmany(5), status = 200)

class BrandedTextSearch(APIView):
    def get(self, request):
        search_string = request.query_params.get("search_string")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT rxcui1 WHERE rela = %s AND ", 
                ["is_tradename", search_string]
            )

"""

class GetID(APIView):
    def get(self, request):
        search_string = request.query_params.get("query")
        #print(search_string)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT str, rxcui FROM rxnconso WHERE str LIKE %s",
                [f"%{search_string}%"]
            )
            temp_results = cursor.fetchall()
        temp_results = sorted(temp_results, key=lambda x: len(x[0]))[:5]
        formated_results = []
        for idx, res_id in enumerate(temp_results):
            formated_results.append({"id": res_id[1], "name": res_id[0]})
        #print(formated_results)
        return Response(formated_results, status = 200)
    
class CreateResultID(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        with connection.cursor() as cursor:
            cursor.execute("SELECT result_id FROM results")
            rows = cursor.fetchall()

            if len(rows) == 0:  # No results yet
                cursor.execute("INSERT INTO results (dt_generated, result_name, result_id, user_id) VALUES " \
                                "(NOW(), %s, %s, %s)", 
                                [1, 1, user_id])
                return Response(status = 200)
            max_id = max(*rows)
            #print(max_id[0])

            # Check if user has any results
            cursor.execute("SELECT result_name FROM results WHERE user_id = %s", 
                           [user_id])
            rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.execute("INSERT INTO results (dt_generated, result_name, result_id, user_id) VALUES " \
                                "(NOW(), %s, %s, %s)", 
                                [1, max_id[0] + 1, user_id])
                return Response(status = 200)
            max_result_name = max(*rows)
            cursor.execute("INSERT INTO results (dt_generated, result_name, result_id, user_id) VALUES " \
            "(NOW(), %s, %s, %s)",
            [int(max_result_name[0]) + 1, max_id[0] + 1, user_id])

            #print(max_id)
        return Response(status = 200)

class DrugConditionsView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        query = """
            SELECT junction.result_id, drug_1_concept_name, drug_2_concept_name, MAX(mean_reporting_frequency)
            FROM Results
            JOIN junction ON Results.result_id = junction.result_id
            LEFT JOIN Interactions ON junction.rxcui1 = interactions.rxcui1
            WHERE ((junction.RXCUI2 = Interactions.RXCUI2) OR 
                   (junction.RXCUI2 = Interactions.RXCUI1))
              AND user_id = %s
            GROUP BY junction.result_id, drug_1_concept_name, drug_2_concept_name
            ORDER BY junction.result_id;
        """
 
        try:
            results = {}
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id])
                for row in cursor.fetchall():
                    result_id = row[0]
                    interaction = {
                        "drug_1_concept_name": row[1],
                        "drug_2_concept_name": row[2],
                        "mean_reporting_frequency": row[3],
                    }
                    if result_id not in results:
                        results[result_id] = []
                    results[result_id].append(interaction)

            # Transform dict into list of {result_id, interactions}
            nested_results = [{"result_id": key, "interactions": value} for key, value in results.items()]
            return Response(nested_results, status=200)
        
        except:
            return Response({"error": "An error occurred"}, status=500)

class UserDrugsView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        query = """
            SELECT DISTINCT RXCUI, union_table.result_id FROM
            (SELECT RXCUI1 AS RXCUI, result_id
            FROM Junction
            UNION
            SELECT RXCUI2 AS RXCUI, result_id
            FROM Junction) AS union_table
            JOIN Results ON union_table.result_id = Results.result_id
            WHERE user_id = %s;
        """

        try:
            results = []
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id])
                # cursor.callproc('GetUserDrugs', [user_id])
                rows = cursor.fetchall()
                print(rows)

                for row in rows:
                    results.append({
                        "RXCUI": row[0], 
                        "result_id": row[1]
                    })
                return Response(results, status = 200)
        except:
            return Response({"error": "An error occurred"}, status=500)
        
class PasswordChangeView(APIView):
    def put(self, request):
        user_id = request.data.get('user_id')
        new_password = request.data.get('password_hash')

        print(user_id, new_password)

        query = """
            UPDATE Users
            SET password_hash = %s
            WHERE user_id = %s;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [new_password, user_id])
                return Response({"message": "Password changed successfully"}, status=200)
        except:
            return Response({"error": "An error occurred"}, status=500)