Feature: Database Performance Testing
  As a test engineer
  I want to validate database performance
  So that I can ensure the system meets performance requirements

  Background:
    Given the database is initialized
    And performance monitoring is enabled

  Scenario: Bulk user creation performance
    Given the database is connected
    When I create 1000 users in bulk
    Then the operation should complete within 5 seconds
    And all users should be created successfully
    And the user count should be 1003

  Scenario: Query performance with large dataset
    Given the database is connected
    And there are 10000 users in the database
    When I search for users with email domain "example.com"
    Then the query should complete within 2 seconds
    And the results should be accurate

  Scenario: Concurrent database operations
    Given the database is connected
    When I perform 50 concurrent read operations
    And I perform 10 concurrent write operations
    Then all operations should complete successfully
    And no deadlocks should occur
    And the total time should be less than 30 seconds

  Scenario: Database connection pool performance
    Given the database connection pool is configured
    When I request 100 database connections simultaneously
    Then all connections should be obtained within 3 seconds
    And all connections should be valid
    And the connection pool should not be exhausted

  Scenario: Large result set handling
    Given the database is connected
    And there are 50000 products in the database
    When I query all products without pagination
    Then the query should handle the large result set
    And memory usage should remain within acceptable limits
    And the query should complete within 10 seconds

  Scenario: Index performance validation
    Given the database is connected
    And indexes are created on frequently queried columns
    When I perform queries on indexed columns
    Then the query execution time should be optimized
    And the query plan should use the indexes

  Scenario: Database backup and restore performance
    Given the database is connected
    And the database contains significant test data
    When I perform a database backup
    Then the backup should complete within 60 seconds
    And the backup file should be created successfully
    When I restore the database from backup
    Then the restore should complete within 90 seconds
    And all data should be restored accurately

  Scenario Outline: Query performance benchmarks
    Given the database is connected
    And there are <record_count> records in the <table_name> table
    When I execute a <query_type> query
    Then the query should complete within <max_time> seconds
    
    Examples:
      | table_name | record_count | query_type | max_time |
      | users      | 10000       | select     | 1        |
      | products   | 50000       | select     | 3        |
      | orders     | 100000      | select     | 5        |
      | users      | 10000       | insert     | 2        |
      | products   | 50000       | update     | 4        |
      | orders     | 100000      | delete     | 6        |

  Scenario: Memory usage monitoring
    Given the database is connected
    And memory monitoring is enabled
    When I perform intensive database operations
    Then memory usage should not exceed 500MB
    And there should be no memory leaks
    And garbage collection should be efficient

  Scenario: Database stress testing
    Given the database is connected
    When I run a stress test with 1000 concurrent users
    And each user performs 100 random operations
    Then the database should remain responsive
    And no operations should fail due to resource exhaustion
    And the response time should remain under 5 seconds per operation 