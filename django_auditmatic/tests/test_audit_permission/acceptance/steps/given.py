"""
given steps
"""
from behave import given, use_step_matcher  # pylint: disable=E0611

use_step_matcher("parse")


@given("the user model is configured with allow: any")
def user_model_configured_with_allow_any(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user model is configured with allow: any')


@given("the user model is configured")
def user_model_is_configured(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user model is configured')


@given("the user has the audit permission")
def user_has_audit_permission(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user has the audit permission')


@given("the user does not have the audit permission")
def user_does_not_have_audit_permission(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user does not have the audit permission')