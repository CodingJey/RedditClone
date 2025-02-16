# env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import logging
import sys

# Import your SQLAlchemy Base and models here
from models.base import Base # Assuming this is where your Base is

# Get the Alembic config object
config = context.config

# ... (logging setup remains the same) ...

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True, # Add this for potential SQLite compatibility
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool, # Keep NullPool for async
        future=True # Ensure future=True for async engine
    )

    with connectable.connect() as connection: # Still sync connect here
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True, # Add this for potential SQLite compatibility
        )
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()