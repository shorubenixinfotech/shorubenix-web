import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import settings

def get_connection():
    return psycopg2.connect(settings.DATABASE_URL)

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch_one:
                return cur.fetchone()
            if fetch_all:
                return cur.fetchall()
            conn.commit()
            return None
    finally:
        conn.close()

def init_database():
    """Create tables if they don't exist."""
    print("Initializing PostgreSQL database...")
    
    queries = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "admin_users": """
            CREATE TABLE IF NOT EXISTS admin_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role VARCHAR(20) DEFAULT 'admin',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "services": """
            CREATE TABLE IF NOT EXISTS services (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                icon VARCHAR(50),
                features JSONB DEFAULT '[]',
                price_prefix VARCHAR(20),
                price_value NUMERIC(10, 2),
                is_active BOOLEAN DEFAULT TRUE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "projects": """
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title VARCHAR(200) NOT NULL,
                description TEXT,
                category VARCHAR(50),
                is_featured BOOLEAN DEFAULT FALSE,
                tech JSONB DEFAULT '[]',
                image_url TEXT,
                live_url TEXT,
                github_url TEXT,
                client_name VARCHAR(100),
                status VARCHAR(50) DEFAULT 'active',
                progress INTEGER DEFAULT 0,
                deadline DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "blog_posts": """
            CREATE TABLE IF NOT EXISTS blog_posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                slug VARCHAR(200) UNIQUE NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                image_url TEXT,
                author VARCHAR(100),
                tags JSONB DEFAULT '[]',
                views INTEGER DEFAULT 0,
                read_time INTEGER,
                is_published BOOLEAN DEFAULT FALSE,
                published_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "contacts": """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                subject VARCHAR(200),
                message TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'New',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "system_logs": """
            CREATE TABLE IF NOT EXISTS system_logs (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                description TEXT,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "newsletter_subscribers": """
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "payments": """
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                project_id INTEGER REFERENCES projects(id),
                amount NUMERIC(15, 2) NOT NULL,
                currency VARCHAR(10) DEFAULT 'INR',
                gateway_order_id VARCHAR(100),
                gateway_payment_id VARCHAR(100),
                status VARCHAR(50) DEFAULT 'Pending',
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "user_projects": """
            CREATE TABLE IF NOT EXISTS user_projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                project_id INTEGER REFERENCES projects(id),
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "notifications": """
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title VARCHAR(200) NOT NULL,
                message TEXT,
                type VARCHAR(20) DEFAULT 'info',
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "complaints": """
            CREATE TABLE IF NOT EXISTS complaints (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                subject VARCHAR(200),
                description TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "analytics": """
            CREATE TABLE IF NOT EXISTS analytics (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                user_id INTEGER REFERENCES users(id),
                description TEXT,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    }
    
    conn = get_connection()
    try:
        # We use a separate transaction for each table to allow continuing on failure
        for table_name, query in queries.items():
            try:
                with conn.cursor() as cur:
                    cur.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                if "already exists" in str(e).lower():
                    print(f"Table/Sequence for '{table_name}' already exists, skipping.")
                else:
                    print(f"Error creating table '{table_name}': {e}")
        
        print("PostgreSQL initialization step completed.")
    except Exception as e:
        print(f"Fatal error during database connection: {e}")
    finally:
        conn.close()
