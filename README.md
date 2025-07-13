# BDD Python Database Test Automation Suite

A comprehensive Behavior-Driven Development (BDD) test automation suite for relational database testing using Python and Behave.

## Features

- **BDD Testing Framework**: Uses Behave (Python's Cucumber equivalent) for readable test scenarios
- **Database Testing**: Comprehensive CRUD operations testing for relational databases
- **Multiple Database Support**: SQLite, PostgreSQL, and MySQL support
- **Performance Testing**: Built-in performance and stress testing scenarios
- **Concurrent Testing**: Multi-threaded database operation testing
- **Transaction Testing**: Transaction rollback and commit testing
- **Data Validation**: Data integrity and constraint validation
- **Flexible Configuration**: Environment-based configuration with multiple profiles
- **Detailed Reporting**: HTML and JUnit report generation
- **Test Data Management**: Automated test data setup and cleanup

## Project Structure

```
bdd-database-test-suite/
├── config/
│   ├── database_config.py      # Database connection configuration
│   └── test_config.py          # Test execution configuration
├── features/
│   ├── steps/
│   │   └── database_steps.py   # Step definitions for BDD scenarios
│   ├── environment.py          # Behave environment hooks
│   ├── database_operations.feature      # Main database operation scenarios
│   └── performance_testing.feature     # Performance testing scenarios
├── utils/
│   └── database_utils.py       # Database utilities and models
├── data/                       # Test data files (auto-generated)
├── reports/                    # Test reports (auto-generated)
├── tests/                      # Additional test files
├── requirements.txt            # Python dependencies
├── behave.ini                  # Behave configuration
└── README.md                   # This file
```

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ~/bdd-database-test-suite
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database** (for non-SQLite databases):
   ```bash
   # For PostgreSQL
   createdb test_db
   
   # For MySQL
   mysql -u root -p -e "CREATE DATABASE test_db;"
   ```

## Configuration

The suite supports multiple configuration methods:

### 1. Environment Variables

Set these environment variables to configure the test suite:

```bash
export DB_DRIVER=sqlite          # Database driver (sqlite, postgresql, mysql)
export DB_HOST=localhost         # Database host
export DB_PORT=5432             # Database port
export DB_NAME=test_db          # Database name
export DB_USER=test_user        # Database username
export DB_PASSWORD=test_password # Database password
```

### 2. Configuration Profiles

Use predefined profiles in `config/test_config.py`:

- `local`: SQLite database for local development
- `ci`: Optimized for CI/CD environments
- `staging`: PostgreSQL for staging environment
- `production`: Production-like settings

### 3. Behave Configuration

Modify `behave.ini` to change test execution behavior:

```ini
[behave]
format = pretty
show_timings = true
junit = true
junit_directory = reports/junit
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
behave

# Run specific feature
behave features/database_operations.feature

# Run specific scenario
behave features/database_operations.feature -n "Create a new user"
```

### Test Filtering with Tags

```bash
# Run performance tests only
behave --tags=@performance

# Skip slow tests
behave --tags=~@slow

# Run specific test types
behave --tags=@crud,@validation
```

### Configuration Options

```bash
# Use specific profile
behave -D profile=staging

# Set custom timeout
behave -D timeout=60

# Use different database
behave -D db_driver=postgresql

# Generate reports
behave -D generate_reports=true
```

### Advanced Options

```bash
# Dry run (don't execute, just validate)
behave --dry-run

# Stop on first failure
behave --stop

# Run with specific formatter
behave --format=json --outfile=reports/results.json

# Parallel execution
behave --jobs=4
```

## Test Scenarios

### Database Operations

The `database_operations.feature` file includes:

- **CRUD Operations**: Create, Read, Update, Delete user records
- **Data Validation**: Email format validation, unique constraints
- **Inventory Management**: Product stock tracking
- **Order Processing**: Order creation and history tracking
- **Transaction Management**: Rollback and commit testing
- **Complex Queries**: Multi-table joins and aggregations

### Performance Testing

The `performance_testing.feature` file includes:

- **Bulk Operations**: Creating thousands of records
- **Concurrent Testing**: Multiple simultaneous database operations
- **Query Performance**: Large dataset query optimization
- **Connection Pooling**: Database connection management
- **Stress Testing**: High-load scenarios
- **Memory Management**: Resource usage monitoring

## Database Models

The suite includes predefined models for testing:

```python
# User model
class User:
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool

# Product model
class Product:
    id: int
    name: str
    price: float
    category: str
    in_stock: int
    created_at: datetime

# Order model
class Order:
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    order_date: datetime
    status: str
```

## Sample Test Data

The suite automatically generates test data:

- **Users**: 3 sample users with different profiles
- **Products**: 3 sample products across different categories
- **Orders**: 3 sample orders linking users and products

## Reporting

The suite generates multiple report formats:

### HTML Reports
```bash
behave --format=html --outfile=reports/results.html
```

### JUnit XML Reports
```bash
behave --junit --junit-directory=reports/junit
```

### JSON Reports
```bash
behave --format=json --outfile=reports/results.json
```

## Extending the Suite

### Adding New Scenarios

1. **Create a new feature file** in the `features/` directory:
   ```gherkin
   Feature: New Database Feature
     As a test engineer
     I want to test new functionality
     So that I can ensure it works correctly
   
     Scenario: Test new functionality
       Given the database is connected
       When I perform a new operation
       Then the operation should succeed
   ```

2. **Add corresponding step definitions** in `features/steps/database_steps.py`:
   ```python
   @when('I perform a new operation')
   def step_new_operation(context):
       # Implementation here
       pass
   ```

### Adding New Database Models

1. **Define the model** in `utils/database_utils.py`:
   ```python
   class NewModel(Base):
       __tablename__ = 'new_table'
       
       id = Column(Integer, primary_key=True)
       name = Column(String(100), nullable=False)
       # Add other columns
   ```

2. **Update the initialization** in the same file:
   ```python
   def init_test_database():
       # Existing code...
       Base.metadata.create_all(db_manager.engine)
   ```

### Custom Configuration

Create environment-specific configurations in `config/test_config.py`:

```python
PROFILES["custom"] = TestConfig(
    db_driver="postgresql",
    db_host="custom-db.example.com",
    performance_threshold=3.0,
    # Other settings...
)
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify database credentials
   - Check database service is running
   - Ensure proper permissions

2. **Step Definition Not Found**:
   - Check step definition syntax
   - Verify imports in step files
   - Ensure proper project structure

3. **Performance Test Failures**:
   - Adjust performance thresholds
   - Check system resources
   - Verify database configuration

### Debug Mode

Run tests with debug information:

```bash
behave --logging-level=DEBUG
```

### Test Data Issues

Reset test data manually:

```bash
python -c "from utils.database_utils import *; cleanup_test_database(); init_test_database(); insert_test_data()"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Database Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        behave -D profile=ci --format=junit --junit-directory=reports/junit
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: reports/
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'behave -D profile=ci --format=junit --junit-directory=reports/junit'
            }
        }
        
        stage('Reports') {
            steps {
                publishTestResults testResultsPattern: 'reports/junit/*.xml'
            }
        }
    }
}
```

## Best Practices

1. **Test Isolation**: Each scenario should be independent
2. **Data Management**: Use fresh test data for each test
3. **Performance Monitoring**: Set realistic performance thresholds
4. **Error Handling**: Implement proper error handling in step definitions
5. **Documentation**: Keep scenarios readable and well-documented
6. **Version Control**: Track changes to test scenarios and data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review test logs in the `reports/` directory
- Create an issue in the project repository

---

**Happy Testing!** 🚀 