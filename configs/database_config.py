# configs/database_config.py
import os

EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appadmin:admin@localhost:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
ALEMBIC_CONFIG_PATH = "alembic.ini" # Define alembic config path here