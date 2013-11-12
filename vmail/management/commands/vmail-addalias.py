"""
Add an email alias entry command.
"""

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from vmail.models import Domain, Alias

HELP_TEXT = """
This will create an email aliases, forwarding address, or
catch-all alias (@example.com) by adding an Alias entry
with the given source and destination addresses.

Neither the souce address, nor the destination address is
required to be an existing MailUser. If --create-domain
is used then the domain is also created if it does not exist.

A virtual alias cannot receive mail, but may only forward
mail to other email addresses.  The source address may be
repeated for each destination mailbox to forward to, and
may also forward to a mailbox of the same address to keep
a copy of an email.  A source address may also be missing
the name portion if the destination address is to be a
catch-all mailbox.  Source and destination addresses are
not required to be local, and thus are not necessarily
related to local virtual mailbox users.

        @example.org  >  john@example.org  # catch-all alias
    john@example.org  >  john@example.org  # keep a copy in local mailbox
    john@example.org  >  jeff@example.com  # forward john to jeff
"""


class Command(BaseCommand):
    args = 'owner-domain source-address destination-address [--create-domain]'
    help = (HELP_TEXT)
    option_list = BaseCommand.option_list + (
        make_option('--create-domain',
                    action='store_true',
                    dest='create_domain',
                    default=False,
                    help='Create the domain which will own the alias if it does not already exist.'),
    )

    def handle(self, *args, **options):
        usage = 'Required arguments: source-address destination-address [--create-domain]'
        if len(args) != 3:
            raise CommandError(usage)

        fqdn = args[0].strip().lower()
        source = args[1].strip().lower()

        if fqdn.startswith('@'):
            fqdn = fqdn[1:]

        destination = args[2].strip().lower()
        try:
            validate_email(destination)
        except ValidationError:
            msg = 'Improperly formatted email address: {0}.'.format(destination)
            raise CommandError(msg)

        try:
            domain = Domain.objects.get(fqdn=fqdn)
        except Domain.DoesNotExist:
            if options['create_domain']:
                domain = Domain.objects.create(fqdn=fqdn)
                self.stdout.write('Created domain: {0}.\n'.format(str(domain)))
            else:
                raise CommandError("Domain '{0}', does not exist.".format(fqdn))

        try:
            Alias.objects.create(domain=domain, source=source,
                                 destination=destination)
        except IntegrityError:
            raise CommandError('Alias exists already.')

        self.stdout.write('Success.\n')
