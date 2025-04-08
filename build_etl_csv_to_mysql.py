import requests
from sqlalchemy import create_engine, text
import pandas as pd
import pymysql
from dateutil import parser
import zipfile
import os
import io
import urllib.parse

#Read zip file from data
#Source license: https://www.kaggle.com/datasets/joebeachcapital/fifa-players?resource=download
csv_file_path = "./data/fifa_2022_datasets/players_22.csv"  # Adjust according to extracted content
data = pd.read_csv(csv_file_path,delimiter=',', quotechar='"')
print(data.shape)
print(data.head())

#set-up mysql connection
my_host = ''
my_user = ''
my_password = ''
encoded_password = urllib.parse.quote_plus(my_password)
my_port = ''
my_database = ''

engine = create_engine(f"mysql+pymysql://{my_user}:{encoded_password}@{my_host}:{my_port}/{my_database}")

# Test connection
try:
    with engine.connect() as connection:
        query = text("select * from ecommerce_db.Order_Items;")
        result = connection.execute(query)
        rows = result.fetchall()
        for row in rows:
            print(row)
except Exception as e:
    print(f"Error: {e}")

# Load: Insert into MySQL
data.to_sql(name = 'players_22', con=engine,if_exists="append", index=False)
print("✅ ETL Process Completed Successfully!")
