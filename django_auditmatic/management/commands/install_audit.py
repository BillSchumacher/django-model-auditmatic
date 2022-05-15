"""
    django command to install triggers
"""
from django.core.management.base import BaseCommand

from django_auditmatic.util import install_triggers


class Command(BaseCommand):
    """
    install_triggers command
    """

    help = "Installs audit table and triggers for the configured models."

    def add_arguments(self, parser):
        # parser.add_argument('models', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        install_triggers()
