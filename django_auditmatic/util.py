from collections import defaultdict
from typing import Dict

from django.apps import apps
from django.conf import settings
from django.db.models import Model

from build.lib.django_auditmatic.util import generate_sql


def find_schemas():
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


def get_all_apps_and_models() -> Dict[str, Model]:
    pass


def install_triggers():
    from django.db import connection

    configured_apps = settings.AUDITMATIC["apps"]
    debug = settings.AUDITMATIC.get("debug", False)
    tenant_schemas = find_schemas()
    schema_apps = []
    if tenant_schemas and len(tenant_schemas) > 0:
        if not hasattr(settings, "TENANT_APPS"):
            raise RuntimeError(
                "Detected tenant model but no apps configured for TENANT_APPS setting.0"
            )
        schema_apps = settings.TENANT_APPs

    configured_app_names = []
    configured_model_names = defaultdict(list)
    configured_model_m2m_names = defaultdict(list)
    for configured_app_name, configured_app_models in configured_apps.items():
        lowered_app_name = configured_app_name.lower()
        configured_app_names.append(lowered_app_name)
        for model_name, model_configuration in configured_app_models.items():
            lowered_model_name = model_name.lower()
            configured_model_names[lowered_app_name].append(lowered_model_name)
            m2m_key = f"{lowered_app_name}_{lowered_model_name}"
            model_m2m_configured_names = model_configuration.get("m2m", [])

            # print("m2m names ", model_m2m_configured_names)
            if model_m2m_configured_names == any:
                # type(model_m2m_configured_names) == callable and \

                configured_model_m2m_names[m2m_key].append(any)
                # print("is any")
            else:
                for value in model_m2m_configured_names:
                    configured_model_m2m_names[m2m_key].append(value)

    for model in apps.get_models():
        app_and_model_name = str(model._meta)
        app_name, model_name = app_and_model_name.split(".")
        print(app_name, app_and_model_name)
        if app_name not in configured_app_names:
            continue
        if model_name not in configured_model_names[app_name]:
            continue

        schema = "public"
        if not len(schema_apps):
            process_model(
                configured_model_m2m_names, app_name, model_name, schema, model
            )
            return

        if app_name not in schema_apps:
            process_model(
                configured_model_m2m_names, app_name, model_name, schema, model
            )
            return

        for tenant_schema in tenant_schemas:
            process_model(
                configured_model_m2m_names, app_name, model_name, tenant_schema, model
            )


def process_model(configured_model_m2m_names, app_name, model_name, schema, model):
    generate_sql(app_name, model_name, schema)
    m2m_key = f"{app_name}_{model_name}"
    is_any = False
    m2m_names = configured_model_m2m_names[m2m_key]
    if m2m_names == any or any in m2m_names:
        is_any = True
    else:
        for m2m_name in m2m_names:
            m2m_names.append(
                (
                    m2m_name[0].lower(),
                    m2m_name[1].lower(),
                )
            )

    for field in model._meta.many_to_many:
        name = field.m2m_db_table()
        if not is_any:
            a = field.model._meta.model_name
            b = field.related_model._meta.model_name
            if (a, b) not in m2m_names:
                continue
        stmt = generate_sql(app_name, name, schema, table_name=name)
