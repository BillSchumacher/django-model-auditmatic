"""
then steps
"""
from behave import then, use_step_matcher  # pylint: disable=E0611

use_step_matcher("parse")


@then("result is True")
def result_is_true(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then result is True')


@then("the user model has an audit permission")
def user_model_has_audit_permission(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user model has an audit permission')


@then("result is False")
def result_is_false(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then result is False')