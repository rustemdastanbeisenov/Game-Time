import psycopg2
from tabulate import tabulate

# Database
DB_NAME = "boardgames"
DB_USER = "postgres"
DB_PASS = "SpErAnstERym"
DB_HOST = "localhost"
DB_PORT = "5432"

# Queries
queries = {
    "A Few Example Games": """
        SELECT * FROM games 
        LIMIT 10;
    """,

    "Top Modern Games (2015+)": """
        SELECT BGGId, Name, YearPublished, AvgRating 
        FROM games
        WHERE YearPublished >= 2015
        ORDER BY AvgRating DESC
        LIMIT 10;
    """,

    "Yearly Game Trends (2000+)": """
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

    "Highly Rated by Users": """
        SELECT g.Name,
               ur.Username,
               ur.Rating
        FROM user_ratings ur
        JOIN games g ON ur.BGGId = g.BGGId
        WHERE ur.Rating >= 9
        ORDER BY ur.Rating DESC, g.Name
        LIMIT 10;
    """,
    
    "Most Rated Games": """
        SELECT g.Name,
               COUNT(ur.Rating) AS NumRatings
        FROM games g
        JOIN user_ratings ur ON g.BGGId = ur.BGGId
        GROUP BY g.Name
        ORDER BY NumRatings DESC
        LIMIT 10;
    """,

    "Oldest Games in Database": """
        SELECT Name, YearPublished, AvgRating
        FROM games
        WHERE YearPublished IS NOT NULL
        ORDER BY YearPublished ASC
        LIMIT 10;
    """,

    "Top Rated Classics (Before 2000)": """
        SELECT Name, YearPublished, AvgRating
        FROM games
        WHERE YearPublished < 2000
        ORDER BY AvgRating DESC
        LIMIT 10;
    """,

    "Prolific Reviewers": """
        SELECT Username, COUNT(Rating) AS NumRatings
        FROM user_ratings
        GROUP BY Username
        ORDER BY NumRatings DESC
        LIMIT 10;
    """,

    "Games With Perfect 10s": """
        SELECT g.Name,
               COUNT(*) AS Perfect10s
        FROM user_ratings ur
        JOIN games g ON ur.BGGId = g.BGGId
        WHERE ur.Rating = 10
        GROUP BY g.Name
        ORDER BY Perfect10s DESC
        LIMIT 10;
    """,

    "Average Ratings by Decade": """
        SELECT (YearPublished / 10) * 10 AS Decade,
               COUNT(*) AS NumGames,
               AVG(AvgRating) AS AvgRating
        FROM games
        WHERE YearPublished IS NOT NULL
        GROUP BY Decade
        ORDER BY Decade;
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