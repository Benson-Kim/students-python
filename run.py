import sqlite3

def run_query(query, parameters=None):
    """
    Execute a query directly on the database.
    
    Args:
        query (str): The SQL query to execute.
        parameters (tuple): The parameters for the query (optional).
    """
    try:
        connection = sqlite3.connect("student_management.db")  # Replace with your DB path
        cursor = connection.cursor()

        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        connection.close()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return None

query = "SELECT * FROM Users WHERE role = ?"
parameters = ("student")  # Replace with actual values
results = run_query(query, parameters)
for row in results:
    print(row)