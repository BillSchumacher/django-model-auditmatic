"""
    generate functions
"""
from django_auditmatic.utils.generate.extension import generate_install_hstore
from django_auditmatic.utils.generate.function import generate_function
from django_auditmatic.utils.generate.table import generate_table
from django_auditmatic.utils.generate.trigger import generate_trigger

__all__ = [
    "generate_function",
    "generate_install_hstore",
    "generate_table",
    "generate_trigger",
]
