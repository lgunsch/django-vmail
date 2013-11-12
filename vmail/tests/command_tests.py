"""
Test the virtual mail management commands.
"""

import sys
import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from ..models import MailUser, Domain, Alias


class BaseCommandTestCase(object):
    fixtures = ['vmail_model_testdata.json']

    def setUp(self):
        self.syserr = sys.stderr
        sys.stderr = StringIO.StringIO()

        self.sysout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.sysout

        sys.stderr.close()
        sys.stderr = self.syserr

    def assertSystemExit(self, *args, **opts):
        """
        Apply the given arguments and options to the current command in
        `self.cmd` and ensure that CommandError is raised.  Default
        aurguments `verbosity=0` and `interactive=False` are applied
        if they are not provided.
        """
        default_opts = {'verbosity': 0, 'interactive': False}
        opts = dict(default_opts.items() + opts.items())
        self.assertRaises(CommandError, call_command, self.cmd, *args, **opts)

    def test_bad_arg_len(self):
        """Test that an incorrect # of positional arguments raises an error."""
        self.assertSystemExit(*range(self.arglen - 1))
        self.assertSystemExit(*range(self.arglen + 1))


class TestChangePassword(BaseCommandTestCase, TestCase):

    cmd = 'vmail-chpasswd'
    arglen = 3

    def _test_change_password(self, pk_):
        old_pw = 'password'
        new_pw = 'new_password'

        user = MailUser.objects.get(pk=pk_)
        user.set_password(old_pw)
        user.save()
        self.assertTrue(user.check_password(old_pw))

        call_command(self.cmd, str(user), old_pw, new_pw)
        user = MailUser.objects.get(pk=pk_)
        self.assertTrue(user.check_password(new_pw))

    def test_change_password(self):
        """Validate change password works as expected."""
        self._test_change_password(1)
        self._test_change_password(7)
        self._test_change_password(8)

    def test_bad_old_password(self):
        user = 'john@example.org'
        self.assertSystemExit(user, 'old pw', 'new pw')

    def test_bad_email(self):
        """Test a proper email is required."""
        self.assertSystemExit('', None, None)
        self.assertSystemExit('@', None, None)
        self.assertSystemExit('a@b.c', None, None)
        self.assertSystemExit(' a@b.c ', None, None)

    def test_bad_domain(self):
        """Test a valid domain is required."""
        user = 'john@bad.domain.com'
        self.assertSystemExit(user, 'old pw', 'new pw')

    def test_bad_mailuser(self):
        """Test a valid user is required."""
        user = 'bad_mailuser@example.org'
        self.assertSystemExit(user, 'old pw', 'new pw')


class TestSetPassword(BaseCommandTestCase, TestCase):

    cmd = 'vmail-setpasswd'
    arglen = 2

    def test_bad_email(self):
        """Test a proper email is required."""
        self.assertSystemExit('', None)
        self.assertSystemExit('@', None)
        self.assertSystemExit('a@b.c', None)
        self.assertSystemExit(' a@b.c ', None)

    def test_bad_domain(self):
        """Test a valid domain is required."""
        user = 'john@bad.domain.com'
        self.assertSystemExit(user, 'new pw')

    def test_bad_mailuser(self):
        """Test a valid user is required."""
        user = 'bad_mailuser@example.org'
        self.assertSystemExit(user, 'new pw')

    def _test_change_password(self, pk_):
        old_pw = 'password'
        new_pw = 'new_password'

        user = MailUser.objects.get(pk=pk_)
        user.set_password(old_pw)
        user.save()
        self.assertTrue(user.check_password(old_pw))

        call_command(self.cmd, str(user), new_pw)
        user = MailUser.objects.get(pk=pk_)
        self.assertTrue(user.check_password(new_pw))

    def test_change_password(self):
        """Validate change password works as expected."""
        self._test_change_password(1)
        self._test_change_password(7)
        self._test_change_password(8)


class TestAddMBoxPassword(BaseCommandTestCase, TestCase):

    cmd = 'vmail-addmbox'
    arglen = 1

    def test_bad_email(self):
        """Test a proper email is required."""
        self.assertSystemExit('')
        self.assertSystemExit('@')
        self.assertSystemExit('a@b.c')
        self.assertSystemExit(' a@b.c ')

    def test_user_already_exests(self):
        user = MailUser.objects.get(pk=1)
        self.assertSystemExit(str(user))

    def test_create_user(self):
        domain = Domain.objects.get(pk=1)
        user = 'me'
        call_command(self.cmd, '{0}@{1}'.format(user, domain))
        created_user = MailUser.objects.get(username=user, domain__fqdn=str(domain))
        self.assertEqual(created_user.username, user)
        self.assertEqual(created_user.domain, domain)

    def test_create_user_domain_not_exists(self):
        user = 'me'
        domain = 'unknown.com'
        self.assertSystemExit('{0}@{1}'.format(user, domain))

        call_command(self.cmd, '{0}@{1}'.format(user, domain), create_domain=True)
        created_user = MailUser.objects.get(username=user, domain__fqdn=str(domain))
        self.assertEqual(created_user.username, user)
        self.assertEqual(created_user.domain.fqdn, domain)

    def test_create_user_with_password(self):
        user = 'me'
        domain = 'example.com'
        password = 'my_new_password'
        call_command(self.cmd, '{0}@{1}'.format(user, domain), password=password)
        created_user = MailUser.objects.get(username=user, domain__fqdn=str(domain))
        self.assertTrue(created_user.check_password(password))
        self.assertEqual(created_user.username, user)
        self.assertEqual(created_user.domain.fqdn, domain)


class TestAddAlias(BaseCommandTestCase, TestCase):

    cmd = 'vmail-addalias'
    arglen = 3

    def test_bad_destination_email(self):
        """Test a proper email is required."""
        # Only destination is required to be a valid email address
        self.assertSystemExit(str(self.domain), self.source, '')
        self.assertSystemExit(str(self.domain), self.source, '@')
        self.assertSystemExit(str(self.domain), self.source, 'a@b.c')
        self.assertSystemExit(str(self.domain), self.source, ' a@b.c ')

    def setUp(self):
        super(TestAddAlias, self).setUp()
        self.domain = Domain.objects.get(pk=1)
        self.source = "alice@example.com"
        self.destination = "alice@example.org"

    def test_add_alias(self):
        call_command(self.cmd, str(self.domain), self.source, self.destination)
        self._assert_created()

    def test_add_catchall(self):
        self.source = '@example.com'
        call_command(self.cmd, str(self.domain), self.source, self.destination)
        self._assert_created()

    def test_add_alias_domain_has_at_symbol(self):
        call_command(
            self.cmd, '@{0}'.format(self.domain), self.source, self.destination)
        self._assert_created()

    def _assert_created(self):
        alias = Alias.objects.get(domain__fqdn=str(self.domain),
                                  source=self.source,
                                  destination=self.destination)
        self.assertTrue(alias.active)

    def test_aliase_exists(self):
        call_command(self.cmd, str(self.domain), self.source, self.destination)
        self.assertSystemExit(self.cmd, str(self.domain), self.source, self.destination)
