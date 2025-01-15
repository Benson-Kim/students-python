# app/database.py
import sqlite3

DB_NAME = "student_management.db"

def initialize_db():
    """
    Create the database and tables from the schema if they don't exist.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    expected_tables = ['Users', 'Students', 'Instructors', 'Courses', 'Grades', 'Enrollments']

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = [table[0] for table in cursor.fetchall()]

    missing_tables = [table for table in expected_tables if table not in existing_tables]
    
    if missing_tables:
        with open("schema.sql", "r") as schema_file:
            schema_script = schema_file.read()

        for table in missing_tables:
            table_creation_statement = extract_table_creation_sql(schema_script, table)
            if table_creation_statement:
                cursor.execute(table_creation_statement)

        connection.commit()
        print(f"Database initialized. Missing tables created: {', '.join(missing_tables)}.")
    else:
        print("All tables already exist. Skipping creation.")

    connection.close()

def extract_table_creation_sql(schema_script, table_name):
    """
    Extract the CREATE TABLE statement for a specific table from the schema script.
    """
    statements = schema_script.split(";")
    for statement in statements:
        if f"CREATE TABLE {table_name}" in statement:
            return statement + ";"
    return None

def get_db_cursor():
    """
    Returns a cursor object to interact with the database.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    return cursor, connection 

if __name__ == "__main__":
    initialize_db()
