"""
then steps
"""
from behave import then, use_step_matcher  # pylint: disable=E0611

use_step_matcher("parse")


@then("the statement generated should contain the audit name")
def generated_statement_contains_audit_name(context):
    """
    :type context: behave.runner.Context
    """
    context.test.assertTrue(context.audit_name in context.statement_generated)


@then("the statement generated should contain the table name")
def generated_statement_contains_table_name(context):
    """
    :type context: behave.runner.Context
    """
    context.test.assertTrue(context.audit_name in context.statement_generated)


@then("the statement generated should contain hstore")
def generated_statement_contains_hstore(context):
    """
    :type context: behave.runner.Context
    """
    context.test.assertTrue("hstore" in context.statement_generated)
