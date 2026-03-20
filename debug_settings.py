import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from config.settings import settings
print(f"DB_HOST: {settings.DB_HOST}")
print(f"DB_PORT: {settings.DB_PORT}")
print(f"DB_USER: {settings.DB_USER}")
print(f"DB_PASSWORD length: {len(settings.DB_PASSWORD)}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")
if "shobi%402003" in settings.DATABASE_URL:
    print("SUCCESS: DATABASE_URL contains correctly encoded password.")
else:
    print("FAILURE: DATABASE_URL does not contain correctly encoded password.")
