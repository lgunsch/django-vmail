"""
List command to print out all mail users, domains, and aliases.
"""

from django.core.management.base import BaseCommand

HELP_TEXT = """
Print out all mail users, domains, and aliases.
"""

class Command(BaseCommand):
    args = '[--domain|--alias] [filter]'
    help = (HELP_TEXT)

    def handle(self, *args, **kwargs):
        pass