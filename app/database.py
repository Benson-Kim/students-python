# app/database.py
import sqlite3

DB_NAME = "student_management.db"

# app/database.py
def initialize_db():
    """
    Create the database and tables from the schema.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    with open("schema.sql", "r") as schema_file:
        cursor.executescript(schema_file.read())

    connection.commit()
    connection.close()


def get_db_cursor():
    """
    Returns a cursor object to interact with the database.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    return cursor, connection 

if __name__ == "__main__":
    initialize_db()
