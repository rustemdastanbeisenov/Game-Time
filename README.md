# Board Games Project

This project provides a Python script that connects to a PostgreSQL database of board games and runs a set of queries to explore ratings, trends, and user activity.

You can download the dataset at: https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek?resource=download

![ERD]([https://upload.wikimedia.org/wikipedia/commons/3/3d/Chess_board_opening_staunton.jpg](https://media.discordapp.net/attachments/776159465132392458/1421498302154674218/erd.png?ex=68d940f5&is=68d7ef75&hm=92b6a46d21ad664d2279b0d4673edbac6f637e71b25fc332ae35aeced6b9923f&=&format=webp&quality=lossless))

## Requirements

- Python 3.8+
- PostgreSQL database (with `games` and `user_ratings` tables)
- Python libraries:
  - `psycopg2`
  - `tabulate`

## Installation

1. Clone the repository or copy the script into your project.
2. Install dependencies:
   ```bash
   pip install psycopg2 tabulate```
3. Configure database connection in main.py by replacing with your own credentials:
   ```DB_NAME = "boardgames"
DB_USER = "your_username"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"```

## Usage
1. Run from Command Line using:
  ```python main.py```
2. Or run from a preferred IDE
