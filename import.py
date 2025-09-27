import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:SpErAnstERym@localhost:5432/boardgames")

folder = r"D:\data visualisation\archive"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        table_name = os.path.splitext(file)[0]
        print(f"Importing {file} -> {table_name}")

        df = pd.read_csv(path)
        df.to_sql(table_name, engine, if_exists="replace", index=False)