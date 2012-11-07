"""
Set password command for administrators to set the password of existing
mail users.
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from madmin.models import MailUser, Domain


class Command(BaseCommand):

    def handle(self, *args, **options):
        usage = 'Required arguments: <email> <new_password>'
        if len(args) != 2:
            raise CommandError(usage)

        email, password = args
        email = email.strip().lower()

        try:
            validate_email(email)
        except ValidationError:
            raise CommandError('Improperly formatted email address.')

        username, fqdn = email.split('@')
        fqdn = fqdn.strip().lower()
        username = username.strip()

        try:
            domain = Domain.objects.get(fqdn=fqdn)
        except Domain.DoesNotExist:
            raise CommandError('Domain %s does not exist.' % fqdn)

        try:
            user = MailUser.objects.get(username=username, domain=domain)
        except MailUser.DoesNotExist:
            raise CommandError('Username %s does not exist.' % username)

        user.set_password(password)
        user.save()
        self.stdout.write('Successful.')
