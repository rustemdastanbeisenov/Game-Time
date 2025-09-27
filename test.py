import psycopg2
from psycopg2 import OperationalError

# Database connection parameters
DB_NAME = "boardgames"
DB_USER = "postgres"
DB_PASS = "SpErAnstERym"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        connection.close()