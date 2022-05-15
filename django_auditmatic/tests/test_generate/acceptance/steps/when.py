from behave import *

from django_auditmatic.utils.generate import generate_function, generate_trigger, generate_table

use_step_matcher("parse")


@when("the function sql is generated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.statement_generated = generate_function(context.audit_name)


@when("the trigger sql is generated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.statement_generated = generate_trigger(context.audit_name, context.table_name)


@when("the table sql is generated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.statement_generated = generate_table(context.audit_name)
