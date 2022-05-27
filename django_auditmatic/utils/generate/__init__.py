"""
    generate functions
"""
from typing import Optional

from django_auditmatic.utils.generate.extension import generate_install_hstore
from django_auditmatic.utils.generate.function import generate_function
from django_auditmatic.utils.generate.table import generate_table
from django_auditmatic.utils.generate.trigger import generate_trigger


def generate_sql(
    app_name: str,
    model_name: str,
    schema: str,
    table_name: Optional[str] = None,
    debug: Optional[bool] = True,
):
    """
        generates the sql
    :param app_name:
    :param model_name:
    :param schema:
    :param table_name:
    :param debug:
    :return:
    """
    table_name = table_name or f"{app_name}_{model_name}"
    audit_name = f"{schema}.audit_{table_name}"
    table_name = f"{schema}.{table_name}"

    statement = f"""
    {generate_table(audit_name)}
    {generate_function(audit_name)}
    {generate_trigger(audit_name, table_name, "INSERT")}
    {generate_trigger(audit_name, table_name, "UPDATE")}
    {generate_trigger(audit_name, table_name, "DELETE")}
    """

    if debug:
        print("Statement generated: ", statement)
        print("Model Name:", model_name)
        print("Table Name:", table_name)
        print("Schema: ", schema)

    return statement


__all__ = [
    "generate_function",
    "generate_install_hstore",
    "generate_sql",
    "generate_table",
    "generate_trigger",
]
