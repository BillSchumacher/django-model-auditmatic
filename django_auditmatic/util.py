"""
    database utility functions
"""
from typing import Optional

from django.db import connection
from django.db.models import Model

from django_auditmatic.configuration.data_classes import ConfiguredNames, ModelNames
from django_auditmatic.utils.generate import generate_install_hstore, generate_sql


def get_model_names(
    model: Model, configured_names: ConfiguredNames
) -> Optional[ModelNames]:
    """
        process the model for all configured schemas.
    :param model:
    :param configured_names:
    :return:
    """
    model_names = ModelNames.from_model(model)
    if model_names.app_name not in configured_names.app_names:
        return
    if model_names.model_name not in configured_names.model_names[model_names.app_name]:
        return
    return model_names


def process_model_for_all_schemas(
    model,
    configured_names,
    schema_apps,
    tenant_schemas,
):
    """
        process the model for all configured schemas.
    :param model:
    :param configured_names:
    :param schema_apps:
    :param tenant_schemas:
    :return:
    """
    model_names = ModelNames.from_model(model)
    if model_names.app_name not in configured_names.app_names:
        return
    if model_names.model_name not in configured_names.model_names[model_names.app_name]:
        return

    schema = "public"

    with connection.cursor() as cursor:
        cursor.execute(generate_install_hstore())
        if not len(schema_apps):  # pylint: disable=C1802
            process_model(cursor, configured_names.model_m2m_names, model_names, schema)
            return

        if model_names.app_name not in schema_apps:
            process_model(cursor, configured_names.model_m2m_names, model_names, schema)
            return

        for tenant_schema in tenant_schemas:
            process_model(
                cursor, configured_names.model_m2m_names, model_names, tenant_schema
            )


def process_model(cursor, configured_model_m2m_names, model_names, schema):
    """
        generates sql for the model and any many to many models configured.
    :param cursor:
    :param configured_model_m2m_names:
    :param model_names:
    :param schema:
    :param model:
    :return:
    """
    app_name = model_names.app_name
    model_name = model_names.model_name
    statement = generate_sql(app_name, model_name, schema)

    cursor.execute(statement)
    m2m_key = f"{app_name}_{model_name}"
    is_any = False
    m2m_names = configured_model_m2m_names[m2m_key]
    if m2m_names == any or any in m2m_names:  # pylint: disable=W0143
        is_any = True
    else:
        for m2m_name in m2m_names:
            m2m_names.append(
                (
                    m2m_name[0].lower(),
                    m2m_name[1].lower(),
                )
            )

    for field in model_names.model._meta.many_to_many:
        name = field.m2m_db_table()
        if not is_any:
            model_name = field.model._meta.model_name
            related_model_name = field.related_model._meta.model_name
            if (model_name, related_model_name) not in m2m_names:
                continue
        statement = generate_sql(app_name, name, schema, table_name=name)
        cursor.execute(statement)
