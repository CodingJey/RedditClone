from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import logging
import sys

# Import your SQLAlchemy Base and models here
from models.models import Base

# Get the Alembic config object
config = context.config

# Set up logging BEFORE loading the config from alembic.ini
# (this allows overriding logging via env.py)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("alembic")

# Load the Alembic .ini file's logging configuration (optional)
# This can be commented out if you want full control via Python code
fileConfig(config.config_file_name)

# Add custom handlers/formatters here (example: file logging)
file_handler = logging.FileHandler("alembic.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode (for testing/shell use)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Enable SQL logging for offline mode
        include_sql=True,
    )

    logger.info("Starting OFFLINE migration...")
    with context.begin_transaction():
        context.run_migrations()
    logger.info("OFFLINE migration complete!")

def run_migrations_online():
    """Run migrations in 'online' mode (production use)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # Enable SQL logging for online mode
        echo=True,  # This logs SQL statements to stdout
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Include SQL in logs
            include_sql=True,
        )

        logger.info("Starting ONLINE migration...")
        with context.begin_transaction():
            context.run_migrations()
        logger.info("ONLINE migration complete!")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Get the database URL from alembic.ini
# config.set_main_option('sqlalchemy.url', 'postgresql+psycopg2://appadmin:admin@db/appdb')
