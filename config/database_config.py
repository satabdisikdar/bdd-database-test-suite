import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    host: str = "localhost"
    port: int = 5432
    database: str = "test_db"
    username: str = "test_user"
    password: str = "test_password"
    driver: str = "sqlite"  # sqlite, postgresql, mysql
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Load configuration from environment variables"""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "test_db"),
            username=os.getenv("DB_USER", "test_user"),
            password=os.getenv("DB_PASSWORD", "test_password"),
            driver=os.getenv("DB_DRIVER", "sqlite")
        )
    
    def get_connection_string(self) -> str:
        """Generate database connection string based on driver"""
        if self.driver.lower() == "sqlite":
            return f"sqlite:///{self.database}.db"
        elif self.driver.lower() == "postgresql":
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.driver.lower() == "mysql":
            return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"Unsupported database driver: {self.driver}")

# Default configuration
DEFAULT_CONFIG = DatabaseConfig.from_env() 