# Created by bschumacher at 5/14/22
Feature: Generate Create Trigger SQL
  Generates the sql used to create the trigger for auditing models.

  Scenario: Generate SQL for Trigger
    Given the audit name is test_audit
    And the table name is test_table
    When the trigger sql is generated
    Then the statement generated should contain the audit name
    And the statement generated should contain the table name
