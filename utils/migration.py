# utils/migration.py
from alembic import command
from alembic.config import Config
import logging
from infra.database import Database  # Import Database from infra
from alembic.script import ScriptDirectory
from configs.database_config import ALEMBIC_CONFIG_PATH # Import config path

logger = logging.getLogger("app")

async def run_migrations(database: Database):
    """Runs Alembic migrations only if changes are detected."""
    alembic_cfg = Config(ALEMBIC_CONFIG_PATH) # Use config path from database_config
    alembic_cfg.attributes['db_url'] = database.url

    script = ScriptDirectory.from_config(alembic_cfg)
    current_head = script.get_current_head()

    async with database.engine.begin() as connection:
        context = command.EnvironmentContext(alembic_cfg, connection, script)
        if context.get_current_revision() == current_head:
            logger.info("No database migrations needed, schema up to date.")
            return

    try:
        logger.info("Checking for database migrations...")
        revisions_to_apply = command.revision(
            alembic_cfg,
            autogenerate=True,
            rev_id='migration_check',
            message='Check for schema changes',
            head="head"
        )

        if revisions_to_apply and revisions_to_apply != 'migration_check':
            logger.info("Database migrations found, starting upgrade...")
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations completed successfully.")
        else:
            logger.info("No database migrations needed, schema up to date.")

    except Exception as e:
        logger.error("Migration check/run failed!", exc_info=True)
        logger.error(f"Alembic details: {e}")
        raise