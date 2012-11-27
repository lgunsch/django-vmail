"""
Test the madmin commands.
"""

import sys
import StringIO

from django.core.management import call_command
from django.test import TestCase

from madmin.models import MailUser, Domain


class BaseCommandTestCase(object):
    fixtures = ['madmin_model_testdata.json']

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
        `self.cmd` and ensure that SystemExit is raised, that is,
        ensure that a CommandError was raised.  Default aurguments
        `verbosity=0` and `interactive=False` are applied if they are
        not provided.
        """
        default_opts = {'verbosity': 0, 'interactive': False}
        opts = dict(default_opts.items() + opts.items())
        self.assertRaises(SystemExit, call_command, self.cmd, *args, **opts)

    def test_bad_arg_len(self):
        """Test that an incorrect # of positional arguments raises an error."""
        self.assertSystemExit(*range(self.arglen - 1))
        self.assertSystemExit(*range(self.arglen + 1))


class TestChangePassword(BaseCommandTestCase, TestCase):

    cmd = 'madmin_chpasswd'
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

    cmd = 'madmin_setpasswd'
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

    cmd = 'madmin_addmbox'
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
        call_command(self.cmd, '%s@%s' % (user, domain))
        created_user = MailUser.objects.get(username=user, domain__fqdn=str(domain))
        self.assertEqual(created_user.username, user)
        self.assertEqual(created_user.domain, domain)

    def test_create_user_domain_not_exists(self):
        user = 'me'
        domain = 'unknown.com'
        self.assertSystemExit('%s@%s' % (user, domain))

        call_command(self.cmd, '%s@%s' % (user, domain), create_domain=True)
        created_user = MailUser.objects.get(username=user, domain__fqdn=str(domain))
        self.assertEqual(created_user.username, user)
        self.assertEqual(created_user.domain.fqdn, domain)
