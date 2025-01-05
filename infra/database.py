
# infra/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time

# Configuration for database URLs
EXTERNAL_DATABASE_URL = "postgresql://user:password@external_host:5432/mydatabase"
TEST_DATABASE_URL = "sqlite:///./test.db"

def is_db_reachable(connection_url):
    """
    Checks if the given database connection URL is reachable within 3 seconds.
    """
    try:
        start_time = time.time()
        with psycopg2.connect(connection_url, connect_timeout=3):
            pass
        elapsed_time = time.time() - start_time
        if elapsed_time > 3:
            return False
        return True
    except Exception:
        return False

# Attempt to connect to the external PostgreSQL database
try:
    if is_db_reachable(EXTERNAL_DATABASE_URL):
        engine = create_engine(EXTERNAL_DATABASE_URL)
        engine.connect()  # Test the connection
        print("Connected to the external PostgreSQL database.")
    else:
        raise ConnectionError("Database connection timeout or unreachable.")
except Exception as e:
    print(f"Failed to connect to external PostgreSQL database: {e}. Falling back to the test database.")
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Base for Models
Base = declarative_base()

# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility to Initialize Database
def init_db():
    import models.models  # Ensure models are imported to register with Base
    Base.metadata.create_all(bind=engine)

# Test Database Configuration for Pytest Integration Testing
def get_test_db():
    """
    Provides a session connected to an in-memory SQLite database for testing.
    """
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Create tables in the test database
    import models.models  # Ensure models are imported to register with Base
    Base.metadata.create_all(bind=test_engine)

    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


