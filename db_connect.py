import mariadb
import os
from dotenv import load_dotenv

try:
    connection = mariadb.connect(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=3306,
        database=os.environ['DB_DATABASE']
    )
    print("Connection successful!")
except Exception as e:
    print(f"Unable to connect to database! {e}")
