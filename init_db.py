import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
               email TEXT PRIMARY KEY,
               password TEXT NOT NULL
               );
               """)

conn.commit()
conn.close()