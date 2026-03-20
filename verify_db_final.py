import psycopg2
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from config.settings import settings

print(f"Testing connection to {settings.DB_HOST}:{settings.DB_PORT} as {settings.DB_USER}")
try:
    # Try connecting to the default 'postgres' database to verify password
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        dbname='postgres',
        connect_timeout=5
    )
    print("SUCCESS: Connected to 'postgres' database. Password is correct.")
    conn.close()
    
    # Now try the actual database
    try:
        conn = psycopg2.connect(
            settings.DATABASE_URL,
            connect_timeout=5
        )
        print(f"SUCCESS: Connected to '{settings.DB_NAME}' database.")
        conn.close()
    except Exception as e:
        print(f"FAILURE: Could not connect to '{settings.DB_NAME}': {e}")
        
except Exception as e:
    print(f"FAILURE: Could not connect to 'postgres' database: {e}")
