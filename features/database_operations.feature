Feature: Database Operations
  As a test engineer
  I want to validate database operations
  So that I can ensure data integrity and proper functionality

  Background:
    Given the database is initialized
    And test data is loaded

  Scenario: Create a new user
    Given the database is connected
    When I create a new user with username "test_user" and email "test@example.com"
    Then the user should be created successfully
    And the user count should be 4

  Scenario: Read user data
    Given the database is connected
    And a user exists with username "john_doe"
    When I retrieve the user by username "john_doe"
    Then the user should be found
    And the user email should be "john@example.com"

  Scenario: Update user information
    Given the database is connected
    And a user exists with username "john_doe"
    When I update the user email to "john.doe@newdomain.com"
    Then the user email should be updated successfully
    And the user email should be "john.doe@newdomain.com"

  Scenario: Delete a user
    Given the database is connected
    And a user exists with username "jane_smith"
    When I delete the user with username "jane_smith"
    Then the user should be deleted successfully
    And the user count should be 2

  Scenario: Verify data integrity constraints
    Given the database is connected
    When I try to create a user with duplicate username "john_doe"
    Then the operation should fail with constraint violation
    And the error message should contain "UNIQUE constraint failed"

  Scenario: Validate product inventory
    Given the database is connected
    And products exist in the inventory
    When I check the inventory for product "Laptop"
    Then the product should be in stock
    And the stock count should be 10

  Scenario: Place an order
    Given the database is connected
    And a user exists with username "john_doe"
    And a product exists with name "Mouse"
    When I place an order for 3 units of "Mouse"
    Then the order should be created successfully
    And the order total should be 77.97

  Scenario: Check order history
    Given the database is connected
    And orders exist for user "john_doe"
    When I retrieve order history for user "john_doe"
    Then I should see the order details
    And the order count should be greater than 0

  Scenario Outline: Database table operations
    Given the database is connected
    When I perform a "<operation>" on table "<table_name>"
    Then the operation should be "<result>"
    
    Examples:
      | operation     | table_name | result     |
      | count         | users      | successful |
      | count         | products   | successful |
      | count         | orders     | successful |
      | schema        | users      | successful |
      | truncate      | orders     | successful |

  Scenario: Database connection handling
    Given the database is not connected
    When I attempt to connect to the database
    Then the connection should be established successfully
    And the database should be accessible

  Scenario: Database transaction rollback
    Given the database is connected
    And a user exists with username "bob_wilson"
    When I start a transaction
    And I update the user email to "bob.updated@example.com"
    And I rollback the transaction
    Then the user email should remain unchanged
    And the user email should be "bob@example.com"

  Scenario: Complex query execution
    Given the database is connected
    And test data is loaded
    When I execute a complex query to get user order statistics
    Then the query should return valid results
    And the results should contain user information with order counts 