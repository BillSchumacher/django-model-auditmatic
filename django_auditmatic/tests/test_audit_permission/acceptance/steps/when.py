"""
when steps
"""
from behave import use_step_matcher, when  # pylint: disable=E0611

use_step_matcher("parse")


@when("the permission validator is called with the user model")
def permission_validator_called_with_user(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the permission validator is called with the user model')