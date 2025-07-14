# BDD Database Test Automation Suite

A comprehensive Behavior-Driven Development (BDD) test automation framework for database operations using Python and Behave.

## Features

### 📋 **Test Coverage**
- **Database Operations**: CRUD operations, transactions, data integrity
- **Performance Testing**: Bulk operations, concurrent access, query optimization
- **DDL Operations**: CREATE, ALTER, DROP, TRUNCATE, Indexes, Constraints
- **DML Operations**: INSERT, UPDATE, DELETE, SELECT with complex queries
- **Error Handling**: Constraint violations, connection failures, data validation

### 🔧 **Technical Stack**
- **Framework**: Behave (Python BDD framework)
- **Database**: SQLite (configurable for PostgreSQL, MySQL)
- **ORM**: SQLAlchemy
- **Testing**: Faker for test data generation
- **Reporting**: JUnit XML, HTML, JSON reports

### 📁 **Project Structure**
```
bdd-database-test-suite/
├── features/
│   ├── database_operations.feature      # Basic CRUD operations
│   ├── performance_testing.feature      # Performance test scenarios
│   ├── ddl_operations.feature          # DDL test scenarios (NEW)
│   ├── dml_operations.feature          # DML test scenarios (NEW)
│   ├── environment.py                  # Test environment setup
│   └── steps/
│       └── database_steps.py           # Step definitions
├── config/
│   ├── database_config.py              # Database configuration
│   └── test_config.py                  # Test configuration
├── utils/
│   └── database_utils.py               # Database utilities
├── run_tests.py                        # Test runner script
└── requirements.txt                    # Dependencies

```

## 🚀 **Getting Started**

### Prerequisites
- Python 3.7+
- Virtual environment support

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/bdd-database-test-suite.git
cd bdd-database-test-suite
```

2. Set up the environment:
```bash
python run_tests.py --setup
```

3. Validate the setup:
```bash
python run_tests.py --validate
```

### Running Tests

#### Basic Commands
```bash
# Run all tests
venv/bin/python run_tests.py

# Run specific feature
venv/bin/python run_tests.py --feature=ddl_operations.feature

# Run with tags
venv/bin/behave --tags=@ddl
venv/bin/behave --tags=@dml
venv/bin/behave --tags=@performance

# Generate reports
venv/bin/python run_tests.py --generate-reports --junit
```

#### Advanced Options
```bash
# Run with specific database driver
venv/bin/python run_tests.py --db-driver=postgresql

# Run with timeout
venv/bin/python run_tests.py --timeout=60

# Run specific scenario
venv/bin/python run_tests.py --scenario="Create a new table"

# Dry run (validate scenarios)
venv/bin/behave --dry-run
```

## 📊 **Test Categories**

### 1. **DDL Operations** (`features/ddl_operations.feature`)
- **Table Management**: CREATE, ALTER, DROP tables
- **Index Operations**: CREATE, DROP indexes (simple and composite)
- **Constraints**: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL
- **Data Definition**: TRUNCATE, Views, Schema modifications
- **Error Handling**: Constraint violations, invalid operations

**Example Scenarios**:
```gherkin
@ddl @create
Scenario: Create a new table with various column types
  Given no table named "test_employees" exists
  When I create a table "test_employees" with the following columns:
    | name      | type          | constraints          |
    | id        | INTEGER       | PRIMARY KEY          |
    | name      | VARCHAR(100)  | NOT NULL             |
    | email     | VARCHAR(150)  | UNIQUE NOT NULL      |
  Then the table "test_employees" should be created successfully
  And the table "test_employees" should have 3 columns

@ddl @truncate
Scenario: Truncate table data
  Given a table "test_data" exists with 100 rows
  When I truncate table "test_data"
  Then the table "test_data" should be empty
  And the table structure should remain intact
```

### 2. **DML Operations** (`features/dml_operations.feature`)
- **INSERT**: Single records, batch inserts, auto-increment, default values
- **UPDATE**: Single records, batch updates, calculated values, JOIN updates
- **DELETE**: Single records, conditional deletes, bulk deletes
- **SELECT**: Basic queries, filtering, sorting, grouping, aggregation, JOINs
- **Transactions**: COMMIT, ROLLBACK, error handling
- **Performance**: Bulk operations, batch processing

**Example Scenarios**:
```gherkin
@dml @insert
Scenario: Insert single record with all columns
  Given an empty table "test_users" exists
  When I insert a record into "test_users" with values:
    | column    | value            |
    | name      | John Doe         |
    | email     | john@example.com |
    | age       | 30               |
  Then the record should be inserted successfully
  And the table "test_users" should have 1 record

@dml @select
Scenario: Select with WHERE condition
  Given a table "test_employees" exists with sample data
  When I select records from "test_employees" where salary > 50000
  Then the query should return only matching records
  And all returned records should have salary greater than 50000
```

### 3. **Performance Testing** (`features/performance_testing.feature`)
- **Bulk Operations**: Large dataset handling
- **Concurrent Access**: Multi-user scenarios
- **Query Performance**: Execution time validation
- **Memory Usage**: Resource consumption monitoring

### 4. **Database Operations** (`features/database_operations.feature`)
- **CRUD Operations**: Create, Read, Update, Delete
- **Data Integrity**: Constraint validation
- **Transaction Management**: ACID compliance
- **Connection Handling**: Database connectivity

## 🎯 **Key Features**

### Comprehensive Test Assertions
- **DDL Assertions**: Table existence, column counts, constraint validation
- **DML Assertions**: Record counts, data accuracy, performance metrics
- **Error Assertions**: Exception handling, constraint violations
- **Performance Assertions**: Execution time, resource usage

### Test Data Management
- **Faker Integration**: Realistic test data generation
- **Database Seeding**: Consistent test data setup
- **Data Cleanup**: Automatic cleanup between scenarios
- **Transaction Isolation**: Independent test execution

### Reporting & Analysis
- **Multiple Formats**: Pretty, JSON, HTML, JUnit XML
- **Performance Metrics**: Query execution times, resource usage
- **Failure Analysis**: Detailed error reporting
- **Test Coverage**: Comprehensive scenario coverage

## 🔧 **Configuration**

### Database Configuration (`config/database_config.py`)
```python
DEFAULT_CONFIG = {
    'driver': 'sqlite',
    'database': 'test.db',
    'host': 'localhost',
    'port': 5432,
    'username': 'testuser',
    'password': 'testpass'
}
```

### Test Configuration (`config/test_config.py`)
- Environment-specific settings
- Test data configuration
- Performance thresholds
- Timeout settings

## 📈 **Example Output**

```
Feature: DDL (Data Definition Language) Operations
  As a database administrator
  I want to validate DDL operations
  So that I can ensure proper schema management

  ✓ Create a new table with various column types
  ✓ Create index on table columns
  ✓ Truncate table data
  ✓ Drop table safely

Feature: DML (Data Manipulation Language) Operations
  As a database user
  I want to validate DML operations
  So that I can ensure proper data manipulation

  ✓ Insert single record with all columns
  ✓ Update multiple records with condition
  ✓ Select with WHERE condition
  ✓ Delete records with complex conditions

2 features passed, 0 failed
8 scenarios passed, 0 failed
24 steps passed, 0 failed
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add your test scenarios
4. Implement step definitions
5. Run tests to ensure functionality
6. Submit a pull request

## 📝 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 **Support**

- **Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and examples
- **Community**: Discussion forums and support channels

---

**Built with ❤️ for comprehensive database testing** 