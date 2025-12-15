import asyncpg
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class PostgresService:
    """
    Service for managing database connections to Neon Postgres
    """

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.database_url = os.getenv("DATABASE_URL")

    async def connect(self):
        """Establish connection to the database"""
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        self.pool = await asyncpg.create_pool(
            dsn=self.database_url,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        print("Connected to Postgres database")

    async def disconnect(self):
        """Close the database connection"""
        if self.pool:
            await self.pool.close()

    async def get_pool(self) -> asyncpg.Pool:
        """Get the connection pool"""
        if not self.pool:
            await self.connect()
        return self.pool

# Global instance
postgres_service = PostgresService()