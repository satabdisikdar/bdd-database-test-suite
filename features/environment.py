"""
Environment configuration for Behave BDD tests
Handles test setup, teardown, and global configuration
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.database_utils import init_test_database, cleanup_test_database, insert_test_data, db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def before_all(context):
    """
    Called before all tests run.
    Set up the test environment.
    """
    logger.info("Setting up test environment...")
    
    # Initialize context attributes
    context.test_results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    # Set up database
    try:
        init_test_database()
        logger.info("Test database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize test database: {str(e)}")
        raise
    
    # Global test configuration
    context.config = {
        'database_driver': 'sqlite',
        'timeout': 30,
        'retry_count': 3,
        'performance_threshold': 5.0
    }
    
    logger.info("Test environment setup complete")

def before_feature(context, feature):
    """
    Called before each feature runs.
    Feature-level setup.
    """
    logger.info(f"Starting feature: {feature.name}")
    context.feature_start_time = time.time()
    
    # Feature-specific setup
    if "performance" in feature.name.lower():
        context.performance_mode = True
        logger.info("Performance testing mode enabled")
    else:
        context.performance_mode = False

def before_scenario(context, scenario):
    """
    Called before each scenario runs.
    Scenario-level setup.
    """
    logger.info(f"Starting scenario: {scenario.name}")
    context.scenario_start_time = time.time()
    
    # Reset database state
    try:
        # Clean up any existing data
        db_manager.truncate_table("orders")
        db_manager.truncate_table("users")
        db_manager.truncate_table("products")
        
        # Insert fresh test data
        insert_test_data()
        
        logger.info("Database reset for scenario")
    except Exception as e:
        logger.error(f"Failed to reset database: {str(e)}")
        raise
    
    # Initialize scenario context
    context.scenario_errors = []
    context.scenario_warnings = []
    context.operation_results = []

def after_scenario(context, scenario):
    """
    Called after each scenario runs.
    Scenario-level teardown.
    """
    scenario_duration = time.time() - context.scenario_start_time
    
    if scenario.status == "passed":
        context.test_results['passed'] += 1
        logger.info(f"Scenario PASSED: {scenario.name} (Duration: {scenario_duration:.2f}s)")
    else:
        context.test_results['failed'] += 1
        logger.error(f"Scenario FAILED: {scenario.name} (Duration: {scenario_duration:.2f}s)")
        
        # Log any captured errors
        if hasattr(context, 'scenario_errors') and context.scenario_errors:
            for error in context.scenario_errors:
                logger.error(f"Scenario error: {error}")
    
    context.test_results['total'] += 1
    
    # Clean up scenario-specific resources
    try:
        if hasattr(context, 'transaction_session'):
            context.transaction_session.close()
    except Exception as e:
        logger.error(f"Error during scenario cleanup: {str(e)}")

def after_feature(context, feature):
    """
    Called after each feature runs.
    Feature-level teardown.
    """
    feature_duration = time.time() - context.feature_start_time
    logger.info(f"Feature completed: {feature.name} (Duration: {feature_duration:.2f}s)")
    
    # Feature-specific cleanup
    if hasattr(context, 'performance_mode') and context.performance_mode:
        logger.info("Performance testing mode disabled")

def after_all(context):
    """
    Called after all tests run.
    Global teardown.
    """
    logger.info("Tearing down test environment...")
    
    # Print test summary
    total = context.test_results['total']
    passed = context.test_results['passed']
    failed = context.test_results['failed']
    
    logger.info(f"Test Summary: {passed}/{total} passed, {failed} failed")
    
    if failed > 0:
        logger.warning(f"{failed} test(s) failed!")
    else:
        logger.info("All tests passed!")
    
    # Clean up database
    try:
        cleanup_test_database()
        logger.info("Test database cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during database cleanup: {str(e)}")
    
    logger.info("Test environment teardown complete")

# Hook for capturing step failures
def after_step(context, step):
    """
    Called after each step runs.
    Capture step failures for debugging.
    """
    if step.status == "failed":
        if hasattr(context, 'scenario_errors'):
            context.scenario_errors.append(f"Step failed: {step.name}")
        
        # Log the exception if available
        if hasattr(step, 'exception'):
            logger.error(f"Step exception: {step.exception}")

# Custom formatters can be added here
def format_step_name(step):
    """Format step name for logging"""
    return f"{step.keyword} {step.name}"

# Add time import that was missing
import time 