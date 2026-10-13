import sys
import os
from pathlib import Path

from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Charge le .env
load_dotenv()

# Ajoute src/ au path pour importer parc_vehicule
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from parc_vehicule.database.database import Base, engine  # noqa: E402

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Pointe vers les métadonnées de Base pour l'autogenerate
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    url = engine.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
