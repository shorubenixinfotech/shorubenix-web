import psycopg2

def test_alt_password():
    # User user's other password
    uri = "postgresql://uh68ejdcgxzosjxmzxl6:shobi@2003@bditexumkeggwqxmthvw-postgresql.services.clever-cloud.com:50013/bditexumkeggwqxmthvw"
    print(f"Testing with alt password: {uri}")
    try:
        conn = psycopg2.connect(uri)
        print("SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_alt_password()
