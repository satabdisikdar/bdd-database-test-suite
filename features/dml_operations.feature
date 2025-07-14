Feature: DML (Data Manipulation Language) Operations
  As a database user
  I want to validate DML operations
  So that I can ensure proper data manipulation and query functionality

  Background:
    Given the database is initialized
    And the database is connected
    And test tables exist for DML operations

  @dml @insert
  Scenario: Insert single record with all columns
    Given an empty table "test_users" exists
    When I insert a record into "test_users" with values:
      | column    | value              |
      | name      | John Doe           |
      | email     | john@example.com   |
      | age       | 30                 |
      | salary    | 50000.00           |
      | is_active | true               |
    Then the record should be inserted successfully
    And the table "test_users" should have 1 record
    And the inserted record should have the correct values

  @dml @insert
  Scenario: Insert multiple records in batch
    Given an empty table "test_products" exists
    When I insert the following records into "test_products":
      | name     | price  | category    | in_stock |
      | Laptop   | 999.99 | Electronics | 10       |
      | Mouse    | 29.99  | Electronics | 50       |
      | Keyboard | 79.99  | Electronics | 25       |
    Then 3 records should be inserted successfully
    And the table "test_products" should have 3 records
    And all records should have the correct values

  @dml @insert
  Scenario: Insert with auto-increment primary key
    Given a table "test_orders" exists with auto-increment id
    When I insert a record into "test_orders" without specifying id:
      | column       | value      |
      | customer_id  | 1          |
      | product_id   | 101        |
      | quantity     | 2          |
      | total_amount | 199.98     |
    Then the record should be inserted successfully
    And the id should be auto-generated
    And the generated id should be greater than 0

  @dml @insert
  Scenario: Insert with default values
    Given a table "test_employees" exists with default values
    When I insert a record into "test_employees" with minimal data:
      | column | value            |
      | name   | Jane Smith       |
      | email  | jane@example.com |
    Then the record should be inserted successfully
    And default values should be applied for unspecified columns
    And the "is_active" column should have default value "true"

  @dml @insert
  Scenario: Insert with null values
    Given a table "test_customers" exists with nullable columns
    When I insert a record into "test_customers" with null values:
      | column      | value               |
      | name        | Anonymous Customer  |
      | email       | NULL                |
      | phone       | NULL                |
      | address     | 123 Main St         |
    Then the record should be inserted successfully
    And the null values should be stored correctly

  @dml @update
  Scenario: Update single record by primary key
    Given a table "test_users" exists with sample data
    And a user with id 1 exists
    When I update the record with id 1 in "test_users" with:
      | column | value                |
      | email  | newemail@example.com |
      | salary | 55000.00             |
    Then the record should be updated successfully
    And 1 record should be affected
    And the record with id 1 should have the updated values

  @dml @update
  Scenario: Update multiple records with condition
    Given a table "test_employees" exists with sample data
    And there are employees with department "Sales"
    When I update all records in "test_employees" where department is "Sales" with:
      | column | value |
      | salary | 60000 |
    Then the records should be updated successfully
    And all "Sales" employees should have salary 60000
    And employees from other departments should remain unchanged

  @dml @update
  Scenario: Update with calculated values
    Given a table "test_products" exists with sample data
    When I update all records in "test_products" to increase price by 10%:
      | column | value            |
      | price  | price * 1.1      |
    Then the records should be updated successfully
    And all prices should be increased by 10%

  @dml @update
  Scenario: Update with joins
    Given tables "test_orders" and "test_customers" exist with related data
    When I update "test_orders" to set customer_name based on customer_id join with "test_customers"
    Then the records should be updated successfully
    And customer names should be populated correctly in orders

  @dml @delete
  Scenario: Delete single record by primary key
    Given a table "test_users" exists with sample data
    And a user with id 5 exists
    When I delete the record with id 5 from "test_users"
    Then the record should be deleted successfully
    And 1 record should be affected
    And the record with id 5 should not exist

  @dml @delete
  Scenario: Delete multiple records with condition
    Given a table "test_products" exists with sample data
    And there are products with category "Discontinued"
    When I delete all records from "test_products" where category is "Discontinued"
    Then the records should be deleted successfully
    And no products with category "Discontinued" should exist
    And products from other categories should remain unchanged

  @dml @delete
  Scenario: Delete with complex conditions
    Given a table "test_orders" exists with sample data
    When I delete all records from "test_orders" where:
      | condition                         |
      | order_date < '2023-01-01'         |
      | AND status = 'cancelled'          |
    Then the records should be deleted successfully
    And only old cancelled orders should be removed
    And recent orders should remain unchanged

  @dml @delete
  Scenario: Delete all records (truncate alternative)
    Given a table "test_temp_data" exists with sample data
    When I delete all records from "test_temp_data"
    Then all records should be deleted successfully
    And the table "test_temp_data" should be empty
    And the table structure should remain intact

  @dml @select
  Scenario: Select all records from table
    Given a table "test_users" exists with 10 records
    When I select all records from "test_users"
    Then the query should return 10 records
    And all columns should be included in the result
    And the records should be returned in correct format

  @dml @select
  Scenario: Select with specific columns
    Given a table "test_products" exists with sample data
    When I select columns "name, price" from "test_products"
    Then the query should return records with only specified columns
    And the result should not include other columns
    And the data should be accurate

  @dml @select
  Scenario: Select with WHERE condition
    Given a table "test_employees" exists with sample data
    When I select records from "test_employees" where salary > 50000
    Then the query should return only matching records
    And all returned records should have salary greater than 50000
    And records with salary <= 50000 should not be included

  @dml @select
  Scenario: Select with multiple conditions
    Given a table "test_orders" exists with sample data
    When I select records from "test_orders" where:
      | condition                    |
      | status = 'completed'         |
      | AND total_amount > 100       |
      | AND order_date >= '2023-01-01' |
    Then the query should return only matching records
    And all returned records should meet all conditions

  @dml @select
  Scenario: Select with ORDER BY
    Given a table "test_products" exists with sample data
    When I select records from "test_products" ordered by price DESC
    Then the query should return records in descending price order
    And the first record should have the highest price
    And the last record should have the lowest price

  @dml @select
  Scenario: Select with LIMIT
    Given a table "test_users" exists with 100 records
    When I select records from "test_users" with limit 10
    Then the query should return exactly 10 records
    And the records should be the first 10 based on default ordering

  @dml @select
  Scenario: Select with GROUP BY and aggregation
    Given a table "test_orders" exists with sample data
    When I select customer_id, COUNT(*) as order_count from "test_orders" grouped by customer_id
    Then the query should return aggregated results
    And each customer should appear only once
    And the order_count should be correct for each customer

  @dml @select
  Scenario: Select with HAVING clause
    Given a table "test_sales" exists with sample data
    When I select product_id, SUM(quantity) as total_sold from "test_sales" grouped by product_id having total_sold > 100
    Then the query should return only products with total sales > 100
    And the aggregated values should be correct

  @dml @select
  Scenario: Select with JOIN operations
    Given tables "test_customers" and "test_orders" exist with related data
    When I select customer name and order details with INNER JOIN
    Then the query should return matched records from both tables
    And customer information should be correctly joined with orders
    And unmatched records should be excluded

  @dml @select
  Scenario: Select with LEFT JOIN
    Given tables "test_customers" and "test_orders" exist with related data
    When I select customer name and order details with LEFT JOIN
    Then the query should return all customers
    And customers without orders should have null values for order columns
    And customers with orders should have correct order information

  @dml @select
  Scenario: Select with subquery
    Given a table "test_employees" exists with sample data
    When I select employees with salary greater than average salary using subquery
    Then the query should return only employees above average salary
    And the subquery should calculate the correct average
    And the results should be accurate

  @dml @select
  Scenario: Select with UNION
    Given tables "test_current_employees" and "test_former_employees" exist
    When I select all employees using UNION of both tables
    Then the query should return combined results
    And duplicate records should be removed
    And the result should include employees from both tables

  @dml @transactions
  Scenario: Successful transaction with multiple DML operations
    Given a table "test_accounts" exists with sample data
    When I start a transaction
    And I update account balance by debiting 100 from account A
    And I update account balance by crediting 100 to account B
    And I commit the transaction
    Then both operations should be successful
    And the total balance should remain unchanged
    And the transaction should be committed

  @dml @transactions
  Scenario: Transaction rollback on error
    Given a table "test_inventory" exists with sample data
    When I start a transaction
    And I update inventory by reducing stock for product X by 10
    And I try to update inventory with invalid data causing error
    And I rollback the transaction
    Then the first operation should be rolled back
    And the inventory should remain unchanged
    And the transaction should be rolled back

  @dml @error_handling
  Scenario: Handle constraint violation on insert
    Given a table "test_unique_emails" exists with unique email constraint
    And a record with email "test@example.com" already exists
    When I try to insert another record with email "test@example.com"
    Then the operation should fail with constraint violation
    And the error message should indicate unique constraint failure
    And the original record should remain unchanged

  @dml @error_handling
  Scenario: Handle foreign key constraint violation
    Given tables "test_departments" and "test_employees" exist with foreign key relationship
    When I try to insert an employee with non-existent department_id
    Then the operation should fail with foreign key constraint violation
    And the error message should indicate foreign key failure
    And no record should be inserted

  @dml @error_handling
  Scenario: Handle data type constraint violation
    Given a table "test_numbers" exists with integer column
    When I try to insert a non-numeric value into integer column
    Then the operation should fail with data type error
    And the error message should indicate data type mismatch
    And no record should be inserted

  @dml @performance
  Scenario: Bulk insert performance
    Given an empty table "test_bulk_data" exists
    When I insert 10000 records into "test_bulk_data" using bulk insert
    Then the operation should complete within 5 seconds
    And all 10000 records should be inserted successfully
    And the bulk insert should be faster than individual inserts

  @dml @performance
  Scenario: Batch update performance
    Given a table "test_large_table" exists with 50000 records
    When I update 10000 records in batches of 1000
    Then the operation should complete within 10 seconds
    And all 10000 records should be updated successfully
    And the batch update should be efficient 