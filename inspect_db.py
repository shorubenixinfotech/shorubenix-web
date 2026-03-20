import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from config.settings import settings
from config.database import execute_query

def check_db():
    print(f"DEBUG: Using DATABASE_URL={settings.DATABASE_URL}")
    tables = ['users', 'admin_users', 'projects', 'services', 'blog_posts', 'contacts', 'payments', 'user_projects']
    for table in tables:
        print(f"\nChecking {table} table...")
        try:
            res = execute_query(f"SELECT COUNT(*) as count FROM {table}", fetch_one=True)
            print(f"Count: {res['count']}")
            if res['count'] > 0:
                rows = execute_query(f"SELECT * FROM {table} LIMIT 5", fetch_all=True)
                # Hide password in debug
                for r in rows:
                    if 'password_hash' in r: r['password_hash'] = '***'
                print(f"Sample data: {rows}")
        except Exception as e:
            print(f"Error checking {table}: {e}")

if __name__ == "__main__":
    check_db()
