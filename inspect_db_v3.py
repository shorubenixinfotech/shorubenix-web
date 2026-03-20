import psycopg2
from psycopg2.extras import RealDictCursor

def check_db():
    print("Testing connection with individual params...")
    try:
        conn = psycopg2.connect(
            host="bditexumkeggwqxmthvw-postgresql.services.clever-cloud.com",
            database="bditexumkeggwqxmthvw",
            user="uh68ejdcgxzosjxmzxl6",
            password="2DOjUOj9P5FSuhAeoQYub8qrxZajCq",
            port=50013
        )
        print("Connected successfully!")
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) as count FROM admin_users")
            res = cur.fetchone()
            print(f"Admin count: {res['count']}")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_db()
