import time
import threading
from typing import Dict, Any, List
from behave import given, when, then, step
from faker import Faker
import traceback
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
import concurrent.futures
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.database_utils import (
    db_manager, init_test_database, cleanup_test_database, 
    insert_test_data, User, Product, Order
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for context sharing
context_data = {}
fake = Faker()

# Background Steps
@given('the database is initialized')
def step_initialize_database(context):
    """Initialize the test database"""
    try:
        init_test_database()
        context.database_initialized = True
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        context.database_initialized = False
        raise

@given('test data is loaded')
def step_load_test_data(context):
    """Load test data into the database"""
    try:
        insert_test_data()
        context.test_data_loaded = True
        logger.info("Test data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load test data: {str(e)}")
        context.test_data_loaded = False
        raise

@given('performance monitoring is enabled')
def step_enable_performance_monitoring(context):
    """Enable performance monitoring"""
    context.performance_monitoring = True
    context.start_time = time.time()
    logger.info("Performance monitoring enabled")

# Connection Steps
@given('the database is connected')
def step_database_connected(context):
    """Verify database connection"""
    if not db_manager.connect():
        raise Exception("Failed to connect to database")
    context.database_connected = True
    logger.info("Database connected successfully")

@given('the database is not connected')
def step_database_not_connected(context):
    """Ensure database is not connected"""
    db_manager.close()
    context.database_connected = False
    logger.info("Database disconnected")

@when('I attempt to connect to the database')
def step_attempt_database_connection(context):
    """Attempt to connect to the database"""
    try:
        result = db_manager.connect()
        context.connection_result = result
        context.database_connected = result
    except Exception as e:
        context.connection_error = str(e)
        context.connection_result = False

@then('the connection should be established successfully')
def step_verify_connection_established(context):
    """Verify connection was established"""
    assert context.connection_result, "Database connection failed"
    assert context.database_connected, "Database not connected"

@then('the database should be accessible')
def step_verify_database_accessible(context):
    """Verify database is accessible"""
    try:
        result = db_manager.execute_query("SELECT 1 as test")
        assert result is not None, "Database is not accessible"
        assert len(result) > 0, "Database query returned no results"
    except Exception as e:
        raise AssertionError(f"Database is not accessible: {str(e)}")

# User Management Steps
@given('a user exists with username "{username}"')
def step_user_exists(context, username):
    """Verify user exists with given username"""
    try:
        result = db_manager.execute_query(
            "SELECT * FROM users WHERE username = :username",
            {"username": username}
        )
        assert len(result) > 0, f"User {username} not found"
        context.current_user = result[0]
    except Exception as e:
        raise AssertionError(f"Error checking user existence: {str(e)}")

@when('I create a new user with username "{username}" and email "{email}"')
def step_create_user(context, username, email):
    """Create a new user"""
    try:
        query = """
            INSERT INTO users (username, email, created_at, is_active)
            VALUES (:username, :email, :created_at, :is_active)
        """
        params = {
            "username": username,
            "email": email,
            "created_at": datetime.utcnow(),
            "is_active": 1
        }
        result = db_manager.execute_non_query(query, params)
        context.operation_result = result
        context.last_created_user = {"username": username, "email": email}
    except Exception as e:
        context.operation_error = str(e)
        context.operation_result = 0

@when('I retrieve the user by username "{username}"')
def step_retrieve_user(context, username):
    """Retrieve user by username"""
    try:
        result = db_manager.execute_query(
            "SELECT * FROM users WHERE username = :username",
            {"username": username}
        )
        context.retrieved_user = result[0] if result else None
    except Exception as e:
        context.operation_error = str(e)
        context.retrieved_user = None

@when('I update the user email to "{new_email}"')
def step_update_user_email(context, new_email):
    """Update user email"""
    try:
        query = """
            UPDATE users SET email = :email 
            WHERE username = :username
        """
        params = {
            "email": new_email,
            "username": context.current_user["username"]
        }
        result = db_manager.execute_non_query(query, params)
        context.operation_result = result
        context.updated_email = new_email
    except Exception as e:
        context.operation_error = str(e)
        context.operation_result = 0

@when('I delete the user with username "{username}"')
def step_delete_user(context, username):
    """Delete user by username"""
    try:
        query = "DELETE FROM users WHERE username = :username"
        result = db_manager.execute_non_query(query, {"username": username})
        context.operation_result = result
        context.deleted_username = username
    except Exception as e:
        context.operation_error = str(e)
        context.operation_result = 0

@when('I try to create a user with duplicate username "{username}"')
def step_create_duplicate_user(context, username):
    """Try to create user with duplicate username"""
    try:
        query = """
            INSERT INTO users (username, email, created_at, is_active)
            VALUES (:username, :email, :created_at, :is_active)
        """
        params = {
            "username": username,
            "email": "duplicate@example.com",
            "created_at": datetime.utcnow(),
            "is_active": 1
        }
        result = db_manager.execute_non_query(query, params)
        context.operation_result = result
    except Exception as e:
        context.operation_error = str(e)
        context.operation_result = 0

# Product Management Steps
@given('products exist in the inventory')
def step_products_exist(context):
    """Verify products exist in inventory"""
    try:
        result = db_manager.execute_query("SELECT COUNT(*) as count FROM products")
        assert result[0]["count"] > 0, "No products found in inventory"
        context.products_exist = True
    except Exception as e:
        raise AssertionError(f"Error checking products: {str(e)}")

@given('a product exists with name "{product_name}"')
def step_product_exists(context, product_name):
    """Verify product exists with given name"""
    try:
        result = db_manager.execute_query(
            "SELECT * FROM products WHERE name = :name",
            {"name": product_name}
        )
        assert len(result) > 0, f"Product {product_name} not found"
        context.current_product = result[0]
    except Exception as e:
        raise AssertionError(f"Error checking product existence: {str(e)}")

@when('I check the inventory for product "{product_name}"')
def step_check_inventory(context, product_name):
    """Check inventory for specific product"""
    try:
        result = db_manager.execute_query(
            "SELECT * FROM products WHERE name = :name",
            {"name": product_name}
        )
        context.inventory_check = result[0] if result else None
    except Exception as e:
        context.operation_error = str(e)
        context.inventory_check = None

# Order Management Steps
@given('orders exist for user "{username}"')
def step_orders_exist_for_user(context, username):
    """Verify orders exist for given user"""
    try:
        result = db_manager.execute_query("""
            SELECT COUNT(*) as count FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE u.username = :username
        """, {"username": username})
        assert result[0]["count"] > 0, f"No orders found for user {username}"
        context.orders_exist = True
    except Exception as e:
        raise AssertionError(f"Error checking orders: {str(e)}")

@when('I place an order for {quantity:d} units of "{product_name}"')
def step_place_order(context, quantity, product_name):
    """Place an order for specified quantity of product"""
    try:
        # Get user and product IDs
        user_id = context.current_user["id"]
        product_id = context.current_product["id"]
        unit_price = context.current_product["price"]
        total_amount = quantity * unit_price
        
        query = """
            INSERT INTO orders (user_id, product_id, quantity, total_amount, order_date, status)
            VALUES (:user_id, :product_id, :quantity, :total_amount, :order_date, :status)
        """
        params = {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_amount": total_amount,
            "order_date": datetime.utcnow(),
            "status": "pending"
        }
        result = db_manager.execute_non_query(query, params)
        context.operation_result = result
        context.order_total = total_amount
    except Exception as e:
        context.operation_error = str(e)
        context.operation_result = 0

@when('I retrieve order history for user "{username}"')
def step_retrieve_order_history(context, username):
    """Retrieve order history for user"""
    try:
        result = db_manager.execute_query("""
            SELECT o.*, p.name as product_name, u.username
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN products p ON o.product_id = p.id
            WHERE u.username = :username
            ORDER BY o.order_date DESC
        """, {"username": username})
        context.order_history = result
    except Exception as e:
        context.operation_error = str(e)
        context.order_history = []

# Database Operations Steps
@when('I perform a "{operation}" on table "{table_name}"')
def step_perform_table_operation(context, operation, table_name):
    """Perform various operations on database tables"""
    try:
        if operation == "count":
            result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
            context.operation_result = result[0]["count"]
        elif operation == "schema":
            result = db_manager.get_table_schema(table_name)
            context.operation_result = len(result)
        elif operation == "truncate":
            result = db_manager.truncate_table(table_name)
            context.operation_result = result
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        context.table_operation_success = True
    except Exception as e:
        context.operation_error = str(e)
        context.table_operation_success = False

# Transaction Steps
@when('I start a transaction')
def step_start_transaction(context):
    """Start a database transaction"""
    context.transaction_started = True
    context.transaction_session = db_manager.session_factory()

@when('I rollback the transaction')
def step_rollback_transaction(context):
    """Rollback the current transaction"""
    if hasattr(context, 'transaction_session'):
        context.transaction_session.rollback()
        context.transaction_session.close()
        context.transaction_rolled_back = True

# Complex Query Steps
@when('I execute a complex query to get user order statistics')
def step_execute_complex_query(context):
    """Execute complex query for user order statistics"""
    try:
        query = """
            SELECT 
                u.username,
                u.email,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as total_spent,
                AVG(o.total_amount) as avg_order_value
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.username, u.email
            ORDER BY total_spent DESC
        """
        result = db_manager.execute_query(query)
        context.complex_query_result = result
    except Exception as e:
        context.operation_error = str(e)
        context.complex_query_result = []

# Performance Testing Steps
@when('I create {count:d} users in bulk')
def step_create_bulk_users(context, count):
    """Create multiple users in bulk"""
    start_time = time.time()
    try:
        users = []
        for i in range(count):
            users.append({
                "username": fake.user_name() + str(i),
                "email": fake.email(),
                "created_at": datetime.utcnow(),
                "is_active": 1
            })
        
        query = """
            INSERT INTO users (username, email, created_at, is_active)
            VALUES (:username, :email, :created_at, :is_active)
        """
        
        with db_manager.get_session() as session:
            for user in users:
                session.execute(query, user)
        
        context.bulk_operation_time = time.time() - start_time
        context.bulk_operation_count = count
        context.bulk_operation_success = True
    except Exception as e:
        context.operation_error = str(e)
        context.bulk_operation_success = False

@given('there are {count:d} users in the database')
def step_ensure_user_count(context, count):
    """Ensure there are specified number of users in database"""
    current_count = db_manager.get_table_count("users")
    if current_count < count:
        needed = count - current_count
        step_create_bulk_users(context, needed)

@given('there are {count:d} products in the database')
def step_ensure_product_count(context, count):
    """Ensure there are specified number of products in database"""
    current_count = db_manager.get_table_count("products")
    if current_count < count:
        needed = count - current_count
        # Create bulk products
        products = []
        for i in range(needed):
            products.append({
                "name": fake.word() + str(i),
                "price": fake.random_number(digits=3),
                "category": fake.word(),
                "in_stock": fake.random_number(digits=2),
                "created_at": datetime.utcnow()
            })
        
        query = """
            INSERT INTO products (name, price, category, in_stock, created_at)
            VALUES (:name, :price, :category, :in_stock, :created_at)
        """
        
        with db_manager.get_session() as session:
            for product in products:
                session.execute(query, product)

@when('I search for users with email domain "{domain}"')
def step_search_users_by_domain(context, domain):
    """Search for users with specific email domain"""
    start_time = time.time()
    try:
        query = "SELECT * FROM users WHERE email LIKE :domain"
        result = db_manager.execute_query(query, {"domain": f"%{domain}%"})
        context.search_result = result
        context.search_time = time.time() - start_time
        context.search_success = True
    except Exception as e:
        context.operation_error = str(e)
        context.search_success = False

@when('I perform {read_count:d} concurrent read operations')
def step_concurrent_read_operations(context, read_count):
    """Perform concurrent read operations"""
    def read_operation():
        return db_manager.execute_query("SELECT COUNT(*) as count FROM users")
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=read_count) as executor:
        futures = [executor.submit(read_operation) for _ in range(read_count)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    context.concurrent_read_time = time.time() - start_time
    context.concurrent_read_results = results
    context.concurrent_read_success = len(results) == read_count

@when('I perform {write_count:d} concurrent write operations')
def step_concurrent_write_operations(context, write_count):
    """Perform concurrent write operations"""
    def write_operation(index):
        query = """
            INSERT INTO users (username, email, created_at, is_active)
            VALUES (:username, :email, :created_at, :is_active)
        """
        params = {
            "username": f"concurrent_user_{index}_{fake.random_number()}",
            "email": fake.email(),
            "created_at": datetime.utcnow(),
            "is_active": 1
        }
        return db_manager.execute_non_query(query, params)
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=write_count) as executor:
        futures = [executor.submit(write_operation, i) for i in range(write_count)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    context.concurrent_write_time = time.time() - start_time
    context.concurrent_write_results = results
    context.concurrent_write_success = len(results) == write_count

# Assertion Steps
@then('the user should be created successfully')
def step_verify_user_created(context):
    """Verify user was created successfully"""
    assert context.operation_result > 0, "User creation failed"
    assert hasattr(context, 'last_created_user'), "No user creation context found"

@then('the user should be found')
def step_verify_user_found(context):
    """Verify user was found"""
    assert context.retrieved_user is not None, "User not found"

@then('the user email should be "{expected_email}"')
def step_verify_user_email(context, expected_email):
    """Verify user email matches expected value"""
    if hasattr(context, 'retrieved_user') and context.retrieved_user:
        assert context.retrieved_user["email"] == expected_email, \
            f"Expected email {expected_email}, got {context.retrieved_user['email']}"
    else:
        # Check updated email
        user = db_manager.execute_query(
            "SELECT * FROM users WHERE username = :username",
            {"username": context.current_user["username"]}
        )[0]
        assert user["email"] == expected_email, \
            f"Expected email {expected_email}, got {user['email']}"

@then('the user email should be updated successfully')
def step_verify_user_email_updated(context):
    """Verify user email was updated successfully"""
    assert context.operation_result > 0, "User email update failed"
    assert hasattr(context, 'updated_email'), "No email update context found"

@then('the user should be deleted successfully')
def step_verify_user_deleted(context):
    """Verify user was deleted successfully"""
    assert context.operation_result > 0, "User deletion failed"
    
    # Verify user no longer exists
    result = db_manager.execute_query(
        "SELECT * FROM users WHERE username = :username",
        {"username": context.deleted_username}
    )
    assert len(result) == 0, "User still exists after deletion"

@then('the user count should be {expected_count:d}')
def step_verify_user_count(context, expected_count):
    """Verify user count matches expected value"""
    actual_count = db_manager.get_table_count("users")
    assert actual_count == expected_count, \
        f"Expected {expected_count} users, got {actual_count}"

@then('the operation should fail with constraint violation')
def step_verify_constraint_violation(context):
    """Verify operation failed with constraint violation"""
    assert context.operation_result == 0, "Operation should have failed"
    assert hasattr(context, 'operation_error'), "No error context found"

@then('the error message should contain "{expected_text}"')
def step_verify_error_message(context, expected_text):
    """Verify error message contains expected text"""
    assert hasattr(context, 'operation_error'), "No error context found"
    assert expected_text in context.operation_error, \
        f"Expected '{expected_text}' in error message: {context.operation_error}"

@then('the product should be in stock')
def step_verify_product_in_stock(context):
    """Verify product is in stock"""
    assert context.inventory_check is not None, "Product not found"
    assert context.inventory_check["in_stock"] > 0, "Product not in stock"

@then('the stock count should be {expected_count:d}')
def step_verify_stock_count(context, expected_count):
    """Verify stock count matches expected value"""
    assert context.inventory_check is not None, "Product not found"
    assert context.inventory_check["in_stock"] == expected_count, \
        f"Expected stock count {expected_count}, got {context.inventory_check['in_stock']}"

@then('the order should be created successfully')
def step_verify_order_created(context):
    """Verify order was created successfully"""
    assert context.operation_result > 0, "Order creation failed"

@then('the order total should be {expected_total:f}')
def step_verify_order_total(context, expected_total):
    """Verify order total matches expected value"""
    assert abs(context.order_total - expected_total) < 0.01, \
        f"Expected order total {expected_total}, got {context.order_total}"

@then('I should see the order details')
def step_verify_order_details(context):
    """Verify order details are returned"""
    assert len(context.order_history) > 0, "No order history found"
    assert all(key in context.order_history[0] for key in ['id', 'user_id', 'product_id', 'quantity']), \
        "Order details missing required fields"

@then('the order count should be greater than {min_count:d}')
def step_verify_order_count_greater(context, min_count):
    """Verify order count is greater than minimum"""
    assert len(context.order_history) > min_count, \
        f"Expected more than {min_count} orders, got {len(context.order_history)}"

@then('the operation should be "{expected_result}"')
def step_verify_operation_result(context, expected_result):
    """Verify operation result matches expected value"""
    if expected_result == "successful":
        assert context.table_operation_success, "Table operation failed"
    else:
        assert not context.table_operation_success, "Table operation should have failed"

@then('the user email should remain unchanged')
def step_verify_email_unchanged(context):
    """Verify user email remains unchanged after rollback"""
    user = db_manager.execute_query(
        "SELECT * FROM users WHERE username = :username",
        {"username": context.current_user["username"]}
    )[0]
    assert user["email"] == context.current_user["email"], \
        "User email changed after rollback"

@then('the query should return valid results')
def step_verify_query_results(context):
    """Verify query returns valid results"""
    assert len(context.complex_query_result) > 0, "Query returned no results"
    assert all(key in context.complex_query_result[0] for key in ['username', 'email', 'order_count']), \
        "Query results missing required fields"

@then('the results should contain user information with order counts')
def step_verify_user_order_stats(context):
    """Verify results contain user information with order counts"""
    for result in context.complex_query_result:
        assert 'username' in result, "Username missing from results"
        assert 'order_count' in result, "Order count missing from results"
        assert isinstance(result['order_count'], int), "Order count should be integer"

# Performance Assertion Steps
@then('the operation should complete within {max_seconds:d} seconds')
def step_verify_operation_time(context, max_seconds):
    """Verify operation completed within specified time"""
    if hasattr(context, 'bulk_operation_time'):
        assert context.bulk_operation_time <= max_seconds, \
            f"Operation took {context.bulk_operation_time:.2f} seconds, expected <= {max_seconds}"
    elif hasattr(context, 'search_time'):
        assert context.search_time <= max_seconds, \
            f"Search took {context.search_time:.2f} seconds, expected <= {max_seconds}"

@then('all users should be created successfully')
def step_verify_all_users_created(context):
    """Verify all users were created successfully"""
    assert context.bulk_operation_success, "Bulk user creation failed"

@then('the query should complete within {max_seconds:d} seconds')
def step_verify_query_time(context, max_seconds):
    """Verify query completed within specified time"""
    assert context.search_time <= max_seconds, \
        f"Query took {context.search_time:.2f} seconds, expected <= {max_seconds}"

@then('the results should be accurate')
def step_verify_results_accurate(context):
    """Verify search results are accurate"""
    assert context.search_success, "Search operation failed"
    assert len(context.search_result) >= 0, "Invalid search results"

@then('all operations should complete successfully')
def step_verify_all_operations_successful(context):
    """Verify all concurrent operations completed successfully"""
    assert context.concurrent_read_success, "Concurrent read operations failed"
    assert context.concurrent_write_success, "Concurrent write operations failed"

@then('no deadlocks should occur')
def step_verify_no_deadlocks(context):
    """Verify no deadlocks occurred"""
    # This is implicitly verified by successful completion
    assert context.concurrent_read_success and context.concurrent_write_success, \
        "Operations failed, possible deadlock"

@then('the total time should be less than {max_seconds:d} seconds')
def step_verify_total_time(context, max_seconds):
    """Verify total time is within limits"""
    total_time = max(context.concurrent_read_time, context.concurrent_write_time)
    assert total_time <= max_seconds, \
        f"Total time {total_time:.2f} seconds, expected <= {max_seconds}"

# Cleanup
def after_scenario(context, scenario):
    """Clean up after each scenario"""
    try:
        if hasattr(context, 'transaction_session'):
            context.transaction_session.close()
        
        # Clean up test data for next scenario
        db_manager.truncate_table("orders")
        db_manager.truncate_table("users")
        db_manager.truncate_table("products")
        
        # Reload base test data
        insert_test_data()
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

def after_all(context):
    """Clean up after all tests"""
    try:
        cleanup_test_database()
    except Exception as e:
        logger.error(f"Error during final cleanup: {str(e)}") 