"""
Chpasswd command for existing mail users to change their password.
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from madmin.models import MailUser, Domain


class Command(BaseCommand):
    args = 'email password new_password'
    help = ('The madmin_chpasswd command changes a mail users password\n'
            'given their email address and current password.  By default\n'
            'the passwords must be supplied in clear-text, and are\n'
            'encrypted by chpasswd.')

    def handle(self, *args, **options):
        usage = 'Required arguments: email password new_password'
        if len(args) != 3:
            raise CommandError(usage)

        email, curr, new = args

        try:
            user = MailUser.get_from_email(email)
        except ValidationError:
            raise CommandError('Improperly formatted email address.')
        except Domain.DoesNotExist:
            raise CommandError('Domain does not exist.')
        except MailUser.DoesNotExist:
            raise CommandError('Username does not exist.')

        authorized = user.check_password(curr)
        if not authorized:
            raise CommandError('Incorrect password.')

        user.set_password(new)
        user.save()
        self.stdout.write('Successful.\n')
