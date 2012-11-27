"""
Set password command for administrators to set the password of existing
mail users.
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from madmin.models import MailUser, Domain


class Command(BaseCommand):
    args = 'email password'
    help = ('The madmin_setpasswd command sets a mail users password given\n'
            'their email address.  The current password is not required.\n'
            'By default the password must be supplied in clear-text.')

    def handle(self, *args, **options):
        usage = 'Required arguments: email new_password'
        if len(args) != 2:
            raise CommandError(usage)

        email, password = args

        try:
            user = MailUser.get_from_email(email)
        except ValidationError:
            raise CommandError('Improperly formatted email address.')
        except Domain.DoesNotExist:
            raise CommandError('Domain does not exist.')
        except MailUser.DoesNotExist:
            raise CommandError('Username does not exist.')

        user.set_password(password)
        user.save()
        self.stdout.write('Successful.\n')
