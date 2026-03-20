import psycopg2

def test_localhost():
    print("Testing localhost:5432 as postgres...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="shobi@2003",
            port=5432
        )
        print("SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_localhost()
