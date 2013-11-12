"""
Set password command for administrators to set the password of existing
mail users.
"""

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from vmail.models import MailUser, Domain


class Command(BaseCommand):
    args = 'email [--create-domain] [--password password]'
    help = ('Create a new MailUser account, with no set password. If\n'
            '--create-domain is used then the domain is also created,\n'
            'given it does not exist. If --password is used then the\n'
            'password is set.')
    option_list = BaseCommand.option_list + (
        make_option('--create-domain',
                    action='store_true',
                    dest='create_domain',
                    default=False,
                    help='Create the domain if it does not already exist.'),
        make_option('--password',
                    dest='password',
                    default=None,
                    help='Set the default password for the user.'),
    )

    def handle(self, *args, **options):
        usage = 'Required arguments: email [--create-domain] [--password password]'
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
                self.stdout.write('Created domain: {0}.\n'.format(str(domain)))
            else:
                raise CommandError('Domain does not exist.')

        user = MailUser.objects.create(username=username, domain=domain)
        if options['password'] is not None:
            user.set_password(options['password'])
            user.save()
            self.stdout.write('Set the password.\n')

        self.stdout.write('Success.\n')
