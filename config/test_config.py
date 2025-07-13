"""
Test configuration settings for the BDD Database Test Suite
"""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TestConfig:
    """Test configuration settings"""
    
    # Database Configuration
    db_driver: str = "sqlite"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "test_db"
    db_user: str = "test_user"
    db_password: str = "test_password"
    
    # Test Configuration
    test_env: str = "local"
    log_level: str = "INFO"
    performance_threshold: float = 5.0
    max_concurrent_connections: int = 100
    timeout_seconds: int = 30
    
    # Database Pool Settings
    db_pool_size: int = 20
    db_pool_max_overflow: int = 30
    db_pool_timeout: int = 30
    
    # Test Data Settings
    load_test_data: bool = True
    cleanup_after_tests: bool = True
    preserve_test_data: bool = False
    
    # Performance Test Settings
    bulk_operation_count: int = 1000
    concurrent_operations: int = 50
    stress_test_users: int = 100
    stress_test_operations: int = 1000
    
    # Reporting Settings
    generate_reports: bool = True
    report_format: str = "html"
    report_output_dir: str = "reports"
    
    @classmethod
    def from_env(cls) -> 'TestConfig':
        """Load configuration from environment variables"""
        return cls(
            db_driver=os.getenv("DB_DRIVER", "sqlite"),
            db_host=os.getenv("DB_HOST", "localhost"),
            db_port=int(os.getenv("DB_PORT", "5432")),
            db_name=os.getenv("DB_NAME", "test_db"),
            db_user=os.getenv("DB_USER", "test_user"),
            db_password=os.getenv("DB_PASSWORD", "test_password"),
            test_env=os.getenv("TEST_ENV", "local"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            performance_threshold=float(os.getenv("PERFORMANCE_THRESHOLD", "5.0")),
            max_concurrent_connections=int(os.getenv("MAX_CONCURRENT_CONNECTIONS", "100")),
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "30")),
            db_pool_size=int(os.getenv("DB_POOL_SIZE", "20")),
            db_pool_max_overflow=int(os.getenv("DB_POOL_MAX_OVERFLOW", "30")),
            db_pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            load_test_data=os.getenv("LOAD_TEST_DATA", "true").lower() == "true",
            cleanup_after_tests=os.getenv("CLEANUP_AFTER_TESTS", "true").lower() == "true",
            preserve_test_data=os.getenv("PRESERVE_TEST_DATA", "false").lower() == "true",
            bulk_operation_count=int(os.getenv("BULK_OPERATION_COUNT", "1000")),
            concurrent_operations=int(os.getenv("CONCURRENT_OPERATIONS", "50")),
            stress_test_users=int(os.getenv("STRESS_TEST_USERS", "100")),
            stress_test_operations=int(os.getenv("STRESS_TEST_OPERATIONS", "1000")),
            generate_reports=os.getenv("GENERATE_REPORTS", "true").lower() == "true",
            report_format=os.getenv("REPORT_FORMAT", "html"),
            report_output_dir=os.getenv("REPORT_OUTPUT_DIR", "reports")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "database": {
                "driver": self.db_driver,
                "host": self.db_host,
                "port": self.db_port,
                "name": self.db_name,
                "user": self.db_user,
                "password": self.db_password,
                "pool_size": self.db_pool_size,
                "pool_max_overflow": self.db_pool_max_overflow,
                "pool_timeout": self.db_pool_timeout
            },
            "test": {
                "environment": self.test_env,
                "log_level": self.log_level,
                "performance_threshold": self.performance_threshold,
                "max_concurrent_connections": self.max_concurrent_connections,
                "timeout_seconds": self.timeout_seconds
            },
            "test_data": {
                "load_test_data": self.load_test_data,
                "cleanup_after_tests": self.cleanup_after_tests,
                "preserve_test_data": self.preserve_test_data
            },
            "performance": {
                "bulk_operation_count": self.bulk_operation_count,
                "concurrent_operations": self.concurrent_operations,
                "stress_test_users": self.stress_test_users,
                "stress_test_operations": self.stress_test_operations
            },
            "reporting": {
                "generate_reports": self.generate_reports,
                "report_format": self.report_format,
                "report_output_dir": self.report_output_dir
            }
        }

# Default configuration instance
TEST_CONFIG = TestConfig.from_env()

# Configuration profiles for different environments
PROFILES = {
    "local": TestConfig(
        db_driver="sqlite",
        db_name="local_test_db",
        performance_threshold=10.0,
        bulk_operation_count=100,
        concurrent_operations=10
    ),
    "ci": TestConfig(
        db_driver="sqlite",
        db_name="ci_test_db",
        performance_threshold=15.0,
        bulk_operation_count=500,
        concurrent_operations=25,
        cleanup_after_tests=True
    ),
    "staging": TestConfig(
        db_driver="postgresql",
        db_host="staging-db.example.com",
        db_name="staging_test_db",
        performance_threshold=5.0,
        bulk_operation_count=1000,
        concurrent_operations=50
    ),
    "production": TestConfig(
        db_driver="postgresql",
        db_host="prod-db.example.com",
        db_name="prod_test_db",
        performance_threshold=2.0,
        bulk_operation_count=2000,
        concurrent_operations=100,
        preserve_test_data=True
    )
}

def get_config(profile: str = None) -> TestConfig:
    """Get configuration for specified profile"""
    if profile and profile in PROFILES:
        return PROFILES[profile]
    return TEST_CONFIG 