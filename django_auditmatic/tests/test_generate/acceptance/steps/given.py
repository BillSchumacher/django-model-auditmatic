"""
given steps
"""
from behave import given, use_step_matcher  # pylint: disable=E0611

use_step_matcher("parse")


@given("the audit name is {audit_name}")
def set_audit_name(context, audit_name: str):
    """
    :type context: behave.runner.Context
    :type audit_name: str
    """
    context.audit_name = audit_name


@given("the table name is {table_name}")
def set_table_name(context, table_name: str):
    """
    :type context: behave.runner.Context
    :type table_name: str
    """
    context.table_name = table_name
