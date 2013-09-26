import sys

from django.core.management.base import BaseCommand, CommandError

from madmin.models import MailUser, Domain


class Command(BaseCommand):
    args = '<email> <curr_password> <new_password>'
    help = ('The madmin_chpasswd command changes a mail users password\n'
            'given their email address and current password.  By default\n'
            'the passwords must be supplied in clear-text, and are\n'
            'encrypted by chpasswd.')

    def handle(self, *args, **options):
        usage = 'Required arguments: <email> <curr_password> <new_password>'
        if len(args) != 3:
            raise CommandError(usage)

        email, curr, new = args

        parts = email.split('@')
        if len(parts) != 2:
            raise CommandError('Improperly formatted email address.')

        username, fqdn = parts

        try:
            domain = Domain.objects.get(fqdn=fqdn.strip())
        except Domain.DoesNotExist:
            raise CommandError('Domain %s does not exist.' % fqdn)
        try:
            user = MailUser.objects.get(username=username.strip(),
                                        domain=domain)
        except MailUser.DoesNotExist:
            raise CommandError('Username %s does not exist.' % username)

        authorized = user.check_password(curr)
        if not authorized:
            raise CommandError('Incorrect password.')

        user.set_password(new)
        user.save()
        self.stdout.write('Successful.')
