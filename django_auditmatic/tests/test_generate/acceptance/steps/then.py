from behave import *

use_step_matcher("parse")


@then("the statement generated should contain the audit name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.test.assertTrue(context.audit_name in context.statement_generated)


@step("the statement generated should contain the table name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.test.assertTrue(context.audit_name in context.statement_generated)
