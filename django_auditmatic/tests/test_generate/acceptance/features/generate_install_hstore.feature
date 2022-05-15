# Created by bschumacher at 5/14/22
Feature: Generate Install HSTORE SQL
  Generates the sql used to install the hstore extension

  Scenario: Generate SQL for installing hstore
    When the hstore sql is generated
    Then the statement generated should contain hstore