from behave import *

use_step_matcher("parse")


@given("the audit name is {audit_name}")
def step_impl(context, audit_name: str):
    """
    :type context: behave.runner.Context
    :type audit_name: str
    """
    context.audit_name = audit_name


@step("the table name is {table_name}")
def step_impl(context, table_name: str):
    """
    :type context: behave.runner.Context
    :type table_name: str
    """
    context.table_name = table_name
