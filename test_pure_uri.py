import psycopg2

def test_pure_uri():
    uri = "postgresql://uh68ejdcgxzosjxmzxl6:2DOjUOj9P5FSuhAeoQYub8qrxZajCq@bditexumkeggwqxmthvw-postgresql.services.clever-cloud.com:50013/bditexumkeggwqxmthvw"
    print(f"Testing pure URI: {uri}")
    try:
        conn = psycopg2.connect(uri)
        print("SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_pure_uri()
