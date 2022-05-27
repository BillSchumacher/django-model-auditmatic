Feature: Audit Permission
  Ideally, this would allow for user specific row level access.
  Initially, grant access based on model level audit permission.

  Scenario: Configure allow: any in model configuration does not restrict access
    Given the user model is configured with allow: any
    And the user exists
    When the audit permission is installed
    When the permission validator is called with the user model
    Then result is True

  Scenario: Configured model has audit permission
    Given the user model is configured
    When the audit permission is installed
    Then the user model has an audit permission

  Scenario: Configured model grants access
    Given the user model is configured
    And the user exists
    And the user has the audit permission
    When the audit permission is installed
    And the permission validator is called with the user model
    Then result is True

  Scenario: Configured model restricts access
    Given the user model is configured
    And the user exists
    And the user does not have the audit permission
    When the audit permission is installed
    And the permission validator is called with the user model
    Then result is False