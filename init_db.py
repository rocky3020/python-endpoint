import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env file")
        return

    # Create engine
    engine = create_engine(DATABASE_URL)

    # SQL for creating the jobs table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        job_type VARCHAR(50) NOT NULL,
        user_wallet VARCHAR(100) NOT NULL,
        amount NUMERIC NOT NULL,
        status VARCHAR(20) DEFAULT 'PENDING',
        tx_hash VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with engine.connect() as conn:
            # Start a transaction and execute
            with conn.begin():
                conn.execute(text(create_table_query))
            print("Successfully connected to Supabase and created/verified 'jobs' table.")
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    init_db()
