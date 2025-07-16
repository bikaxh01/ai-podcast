from sqlmodel import SQLModel
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the database URL from the environment
DB_URL = os.getenv("DATABASE_URL")
print("URL 😁😁😁😁😁",DB_URL)
config = context.config
config.set_main_option("sqlalchemy.url", DB_URL)

# Import your models
from Db.db import User, Podcast

# This function runs migrations
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=SQLModel.metadata)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()