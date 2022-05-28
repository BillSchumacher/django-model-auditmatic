# Created by bschumacher at 5/14/22
Feature: Generate Create Table SQL
  Generates the sql used to create the table for auditing models.

  Scenario: Generate SQL for Table
    Given the audit name is test
    When the table sql is generated
    Then the statement generated should contain the audit name