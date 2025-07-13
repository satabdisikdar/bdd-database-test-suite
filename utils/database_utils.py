import sqlite3
import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

from config.database_config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """Database connection and operation manager"""
    
    def __init__(self, config=None):
        self.config = config or DEFAULT_CONFIG
        self.engine = None
        self.session_factory = None
        self.metadata = MetaData()
        
    def connect(self):
        """Establish database connection"""
        try:
            connection_string = self.config.get_connection_string()
            self.engine = create_engine(connection_string, echo=False)
            self.session_factory = sessionmaker(bind=self.engine)
            logger.info(f"Connected to database: {self.config.driver}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            return False
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        if not self.session_factory:
            self.connect()
        
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute SQL query and return results"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
    
    def execute_non_query(self, query: str, params: Optional[Dict] = None) -> int:
        """Execute non-query SQL statement and return affected rows"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return result.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database"""
        try:
            with self.get_session() as session:
                result = session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
                return result.fetchone() is not None
        except Exception:
            return False
    
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Get table schema information"""
        try:
            with self.get_session() as session:
                result = session.execute(text(f"PRAGMA table_info({table_name})"))
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error getting table schema: {str(e)}")
            return []
    
    def get_table_count(self, table_name: str) -> int:
        """Get number of rows in table"""
        try:
            result = self.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
            return result[0]['count'] if result else 0
        except Exception:
            return 0
    
    def truncate_table(self, table_name: str) -> bool:
        """Truncate table (delete all rows)"""
        try:
            self.execute_non_query(f"DELETE FROM {table_name}")
            return True
        except Exception as e:
            logger.error(f"Error truncating table {table_name}: {str(e)}")
            return False
    
    def drop_table(self, table_name: str) -> bool:
        """Drop table if exists"""
        try:
            self.execute_non_query(f"DROP TABLE IF EXISTS {table_name}")
            return True
        except Exception as e:
            logger.error(f"Error dropping table {table_name}: {str(e)}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

# Sample table models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    in_stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')

# Global database manager instance
db_manager = DatabaseManager()

def init_test_database():
    """Initialize test database with sample tables"""
    if not db_manager.connect():
        raise Exception("Failed to connect to database")
    
    # Create all tables
    Base.metadata.create_all(db_manager.engine)
    logger.info("Test database initialized successfully")

def cleanup_test_database():
    """Clean up test database"""
    try:
        Base.metadata.drop_all(db_manager.engine)
        db_manager.close()
        logger.info("Test database cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up database: {str(e)}")

def insert_test_data():
    """Insert sample test data"""
    try:
        with db_manager.get_session() as session:
            # Insert sample users
            users = [
                User(username="john_doe", email="john@example.com"),
                User(username="jane_smith", email="jane@example.com"),
                User(username="bob_wilson", email="bob@example.com")
            ]
            session.add_all(users)
            session.flush()
            
            # Insert sample products
            products = [
                Product(name="Laptop", price=999.99, category="Electronics", in_stock=10),
                Product(name="Mouse", price=25.99, category="Electronics", in_stock=50),
                Product(name="Book", price=12.99, category="Books", in_stock=30)
            ]
            session.add_all(products)
            session.flush()
            
            # Insert sample orders
            orders = [
                Order(user_id=1, product_id=1, quantity=1, total_amount=999.99),
                Order(user_id=2, product_id=2, quantity=2, total_amount=51.98),
                Order(user_id=3, product_id=3, quantity=3, total_amount=38.97)
            ]
            session.add_all(orders)
            
        logger.info("Test data inserted successfully")
    except Exception as e:
        logger.error(f"Error inserting test data: {str(e)}")
        raise 