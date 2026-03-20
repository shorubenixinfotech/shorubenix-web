import psycopg2

def test_alt_password_pure():
    print("Testing shobi@2003 with individual params...")
    try:
        conn = psycopg2.connect(
            host="bditexumkeggwqxmthvw-postgresql.services.clever-cloud.com",
            database="bditexumkeggwqxmthvw",
            user="uh68ejdcgxzosjxmzxl6",
            password="shobi@2003",
            port=50013
        )
        print("SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_alt_password_pure()
