"""
Set password command for administrators to set the password of existing
mail users.
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from vmail.models import MailUser, Domain


class Command(BaseCommand):
    args = 'email password'
    help = ('Sets a mail users password. The current password is not\n'
            'required, and by default, the password must be supplied in\n'
            'clear-text.')

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
        self.stdout.write('Success.\n')
