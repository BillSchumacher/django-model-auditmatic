# Created by bschumacher at 5/14/22
Feature: Generate Create Function SQL
  Generates the sql used to create the function for auditing models.

  Scenario: Generate SQL for Function
    Given the audit name is test
    When the function sql is generated
    Then the statement generated should contain the audit name