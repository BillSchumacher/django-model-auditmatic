from django.apps import AppConfig
from django.conf import settings


class DjangoAuditmaticConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_auditmatic"


if not hasattr(settings, "AUDITMATIC"):
    raise RuntimeError("AUDITMATIC Config not detected.")
