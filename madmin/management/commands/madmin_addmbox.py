"""
Set password command for administrators to set the password of existing
mail users.
"""

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from madmin.models import MailUser, Domain


class Command(BaseCommand):
    args = 'email [--create-domain]'
    help = ('The madmin_addmbox creates a new MailUser account, with no '
            'set password.  If --create-domain is used then the domain '
            'is also created if it does not exist.')
    option_list = BaseCommand.option_list + (
        make_option('--create-domain',
                    action='store_true',
                    dest='create_domain',
                    default=False,
                    help='Create the domain if it does not already exist.'),
    )

    def handle(self, *args, **options):
        usage = 'Required arguments: email [--create-domain]'
        if len(args) != 1:
            raise CommandError(usage)

        email = args[0].strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            raise CommandError('Improperly formatted email address.')

        username, fqdn = email.split('@')
        username = username.strip()

        try:
            MailUser.objects.get(username=username, domain__fqdn=fqdn)
        except MailUser.DoesNotExist:
            pass
        else:
            raise CommandError('Username exist already.')

        try:
            domain = Domain.objects.get(fqdn=fqdn)
        except Domain.DoesNotExist:
            if options['create_domain']:
                domain = Domain.objects.create(fqdn=fqdn)
                self.stdout.write('Created domain: %s.\n' % str(domain))
            else:
                raise CommandError('Domain does not exist.')


        MailUser.objects.create(username=username, domain=domain)
        self.stdout.write('Successful.\n')
