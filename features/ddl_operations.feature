Feature: DDL (Data Definition Language) Operations
  As a database administrator
  I want to validate DDL operations
  So that I can ensure proper schema management and database structure integrity

  Background:
    Given the database is initialized
    And the database is connected

  @ddl @create
  Scenario: Create a new table with various column types
    Given no table named "test_employees" exists
    When I create a table "test_employees" with the following columns:
      | name        | type         | constraints           |
      | id          | INTEGER      | PRIMARY KEY          |
      | name        | VARCHAR(100) | NOT NULL             |
      | email       | VARCHAR(150) | UNIQUE NOT NULL      |
      | age         | INTEGER      | CHECK (age >= 18)    |
      | salary      | DECIMAL(10,2)| DEFAULT 0.00         |
      | hire_date   | DATE         | DEFAULT CURRENT_DATE |
      | is_active   | BOOLEAN      | DEFAULT TRUE         |
    Then the table "test_employees" should be created successfully
    And the table "test_employees" should have 7 columns
    And the table "test_employees" should have primary key on "id"
    And the table "test_employees" should have unique constraint on "email"

  @ddl @create
  Scenario: Create table with foreign key constraint
    Given a table "departments" exists with columns:
      | name    | type         | constraints |
      | id      | INTEGER      | PRIMARY KEY |
      | name    | VARCHAR(100) | NOT NULL    |
    When I create a table "employees_with_dept" with the following columns:
      | name        | type         | constraints                                    |
      | id          | INTEGER      | PRIMARY KEY                                   |
      | name        | VARCHAR(100) | NOT NULL                                      |
      | department_id| INTEGER     | FOREIGN KEY REFERENCES departments(id)       |
    Then the table "employees_with_dept" should be created successfully
    And the foreign key constraint should be active on "department_id"

  @ddl @create
  Scenario: Create index on table columns
    Given a table "test_customers" exists with sample data
    When I create an index "idx_customer_email" on table "test_customers" column "email"
    Then the index "idx_customer_email" should be created successfully
    And the index should improve query performance on "email" column

  @ddl @create
  Scenario: Create composite index
    Given a table "test_orders" exists with sample data
    When I create a composite index "idx_order_date_status" on table "test_orders" columns "order_date, status"
    Then the composite index "idx_order_date_status" should be created successfully
    And the index should be usable for queries on both columns

  @ddl @alter
  Scenario: Add new column to existing table
    Given a table "test_products" exists with basic columns
    When I add a new column "description" of type "TEXT" to table "test_products"
    Then the column "description" should be added successfully
    And the table "test_products" should have the new column "description"
    And existing data in the table should remain intact

  @ddl @alter
  Scenario: Add column with default value
    Given a table "test_users" exists with sample data
    When I add a new column "status" of type "VARCHAR(20)" with default value "active" to table "test_users"
    Then the column "status" should be added successfully
    And all existing rows should have "status" value as "active"

  @ddl @alter
  Scenario: Add constraint to existing table
    Given a table "test_products" exists without constraints
    When I add a unique constraint "unique_product_code" on column "product_code"
    Then the constraint should be added successfully
    And duplicate values should be prevented in "product_code" column

  @ddl @alter
  Scenario: Rename table
    Given a table "old_table_name" exists with data
    When I rename table "old_table_name" to "new_table_name"
    Then the table "new_table_name" should exist
    And the table "old_table_name" should not exist
    And all data should be preserved in "new_table_name"

  @ddl @drop
  Scenario: Drop table safely
    Given a table "temporary_table" exists with data
    When I drop table "temporary_table"
    Then the table "temporary_table" should not exist
    And no error should occur during the drop operation

  @ddl @drop
  Scenario: Drop table with cascade (foreign key dependencies)
    Given a table "parent_table" exists with data
    And a table "child_table" exists with foreign key reference to "parent_table"
    When I drop table "parent_table" with cascade
    Then the table "parent_table" should not exist
    And dependent relationships should be handled properly

  @ddl @drop
  Scenario: Drop index
    Given a table "test_table" exists with an index "test_index"
    When I drop index "test_index"
    Then the index "test_index" should not exist
    And the table "test_table" should remain unchanged

  @ddl @drop
  Scenario: Drop column from table
    Given a table "test_table" exists with column "unwanted_column"
    When I drop column "unwanted_column" from table "test_table"
    Then the column "unwanted_column" should not exist in table "test_table"
    And other columns should remain intact

  @ddl @truncate
  Scenario: Truncate table data
    Given a table "test_data" exists with 100 rows
    When I truncate table "test_data"
    Then the table "test_data" should be empty
    And the table structure should remain intact
    And the operation should be faster than individual deletes

  @ddl @truncate
  Scenario: Truncate table with auto-increment reset
    Given a table "test_sequence" exists with auto-increment column
    And the table has data with highest id value of 50
    When I truncate table "test_sequence"
    Then the table should be empty
    And the auto-increment counter should reset to 1

  @ddl @constraints
  Scenario: Add check constraint
    Given a table "test_employees" exists
    When I add a check constraint "valid_age" that ensures "age > 0 AND age < 150"
    Then the constraint should be added successfully
    And invalid age values should be rejected

  @ddl @constraints
  Scenario: Add not null constraint
    Given a table "test_table" exists with nullable column "required_field"
    When I add a not null constraint to column "required_field"
    Then the constraint should be added successfully
    And null values should be rejected for "required_field"

  @ddl @views
  Scenario: Create database view
    Given tables "users" and "orders" exist with sample data
    When I create a view "user_order_summary" that joins users and orders
    Then the view "user_order_summary" should be created successfully
    And the view should return expected data when queried

  @ddl @views
  Scenario: Drop database view
    Given a view "test_view" exists
    When I drop view "test_view"
    Then the view "test_view" should not exist
    And underlying tables should remain unchanged

  @ddl @error_handling
  Scenario: Handle table creation errors
    Given a table "existing_table" already exists
    When I try to create a table "existing_table" without "IF NOT EXISTS"
    Then the operation should fail with appropriate error
    And the error message should indicate table already exists

  @ddl @error_handling
  Scenario: Handle column addition errors
    Given a table "test_table" exists with column "existing_column"
    When I try to add a column "existing_column" to table "test_table"
    Then the operation should fail with appropriate error
    And the error message should indicate column already exists

  @ddl @error_handling
  Scenario: Handle foreign key constraint errors
    Given a table "parent_table" does not exist
    When I try to create a table with foreign key reference to "parent_table"
    Then the operation should fail with appropriate error
    And the error message should indicate referenced table does not exist 