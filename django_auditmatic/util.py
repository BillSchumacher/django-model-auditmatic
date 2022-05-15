"""
    database utility functions
"""

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from django.apps import apps
from django.conf import settings
from django.db import connection

from django_auditmatic.utils.generate import (
    generate_function,
    generate_install_hstore,
    generate_table,
    generate_trigger,
)


def find_schemas() -> Optional[List[str]]:
    """
        find all schemas by querying the tenant's schema names.
    :return: List[str]
    """
    if not hasattr(settings, "TENANT_MODEL"):
        return None

    tenant_model_setting = settings.TENANT_MODEL
    split_tenant_model = tenant_model_setting.split(".")
    tenant_model_name = split_tenant_model[-1]
    tenant_model = None
    for model in apps.get_models():
        # print(dir(model))
        # print(model._meta.model_name, tenant_model_setting)
        if model._meta.model_name == tenant_model_name:
            tenant_model = model
    if not tenant_model:
        return None
    return tenant_model.objects.values_list("schema_name", flat=True)


class ConfiguredNames:
    """
    A data object to hold configured name values.
    """

    def __init__(self, app_names: List, model_names: Dict, model_m2m_names: Dict):
        self.app_names = app_names
        self.model_names = model_names
        self.model_m2m_names = model_m2m_names

    @staticmethod
    def process_app_models(
        app_name, app_names, app_models, model_names, model_m2m_names
    ):
        """
            process app configured models
        :param app_name:
        :param app_names:
        :param app_models:
        :param model_names:
        :param model_m2m_names:
        :return:
        """
        lowered_app_name = app_name.lower()
        app_names.append(lowered_app_name)
        for model_name, model_configuration in app_models.items():
            lowered_model_name = model_name.lower()
            model_names[lowered_app_name].append(lowered_model_name)
            m2m_key = f"{lowered_app_name}_{lowered_model_name}"
            model_m2m_configured_names = model_configuration.get("m2m", [])

            # print("m2m names ", model_m2m_configured_names)
            if model_m2m_configured_names == any:  # pylint: disable=W0143
                # type(model_m2m_configured_names) == callable and \

                model_m2m_names[m2m_key].append(any)
                # print("is any")
            else:
                for value in model_m2m_configured_names:
                    model_m2m_names[m2m_key].append(value)

    @staticmethod
    def from_settings():
        """
            creates ConfiguredNames from settings.
        :return:
        """
        configured_apps = settings.AUDITMATIC["apps"]

        app_names = []
        model_names = defaultdict(list)
        model_m2m_names = defaultdict(list)
        for app_name, app_models in configured_apps.items():
            ConfiguredNames.process_app_models(
                app_name, app_names, app_models, model_names, model_m2m_names
            )

        return ConfiguredNames(app_names, model_names, model_m2m_names)


def get_tenant_schemas_and_apps() -> Tuple[List, List]:
    """
        process tenant configuration if tenants are in use.
    :return:
    """
    tenant_schemas = find_schemas()
    schema_apps = []
    if tenant_schemas and len(tenant_schemas) > 0:
        if not hasattr(settings, "TENANT_APPS"):
            raise RuntimeError(
                "Detected tenant model but no apps configured for TENANT_APPS setting."
            )
        schema_apps = settings.TENANT_APPS
    return tenant_schemas, schema_apps


def install_triggers():
    """
        installs the auditing triggers and such for the configured models.
    :return:
    """

    # debug = settings.AUDITMATIC.get("debug", False)
    tenant_schemas, schema_apps = get_tenant_schemas_and_apps()

    configured_names = ConfiguredNames.from_settings()

    for model in apps.get_models():
        process_model_for_all_schemas(
            model,
            configured_names,
            schema_apps,
            tenant_schemas,
        )


class ModelNames:
    """
    a data object that stores info about a model
    """

    def __init__(self, app_name, model_name, model):
        self.app_name = app_name
        self.model_name = model_name
        self.model = model

    @staticmethod
    def from_model(model):
        """generates an object from a model"""
        app_and_model_name = str(model._meta)
        app_name, model_name = app_and_model_name.split(".")
        return ModelNames(app_name, model_name, model)

    def __repr__(self):
        return f"{self.app_name}_{self.model_name}"


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
