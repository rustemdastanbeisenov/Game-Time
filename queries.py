import psycopg2
from tabulate import tabulate

# Database connection parameters
DB_NAME = "boardgames"
DB_USER = "postgres"
DB_PASS = "SpErAnstERym"
DB_HOST = "localhost"
DB_PORT = "5432"

# Queries to run
queries = {
    "Sample Games": """SELECT * FROM games LIMIT 10;""",
    
    "Where filtering": """
        SELECT BGGId, Name, YearPublished, AvgRating 
        FROM games
        WHERE YearPublished >= 2015
        ORDER BY AvgRating DESC
        LIMIT 10;
    """,
    
    "Group by filtering": """
        SELECT YearPublished,
               COUNT(*) AS NumGames,
               AVG(AvgRating) AS AvgRating,
               MIN(AvgRating) AS LowestRating,
               MAX(AvgRating) AS HighestRating
        FROM games
        WHERE YearPublished >= 2000
        GROUP BY YearPublished
        ORDER BY YearPublished;
    """,
    
    "Aggregation": """
        SELECT g.Name,
               ur.Username,
               ur.Rating
        FROM user_ratings ur
        JOIN games g ON ur.BGGId = g.BGGId
        WHERE ur.Rating >= 9
        ORDER BY ur.Rating DESC, g.Name
        LIMIT 10;
    """
}


def run_queries():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Execute each query and print results
        for title, query in queries.items():
            print(f"\n--- {title} ---")
            cur.execute(query)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=colnames, tablefmt="psql"))

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    run_queries()