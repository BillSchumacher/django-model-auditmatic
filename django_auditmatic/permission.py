"""
    audit permission
"""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.conf import settings


class PermissionSettings:
    """
    permission settings data object
    """
    def __init__(self):
        auditmatic_settings = settings.AUDITMATIC
        self.codename = 'can_audit'
        self.name = 'Can Audit'
        permission = auditmatic_settings.get('permission')
        if not permission:
            return

        if permission_codename := permission.get('codename'):
            self.codename = permission_codename
        if permission_name := permission.get('name'):
            self.name = permission_name


permission_settings = PermissionSettings()


def get_or_create_audit_permission(model: Model) -> Permission:
    """
        create an audit permission for the given model.
    :param model:
    :return:
    """
    content_type = ContentType.objects.get_for_model(model)
    return Permission.objects.get_or_create(
        codename=permission_settings.codename,
        name=f'{permission_settings.name} {model._meta.object_name}',
        content_type=content_type,
    )
