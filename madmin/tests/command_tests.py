"""
Test the madmin commands.
"""

import sys
import StringIO

from django.core.management import call_command
from django.test import TestCase

from madmin.models import MailUser


class TestChangePassword(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def setUp(self):
        self.cmd = 'madmin_chpasswd'

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

    def test_bad_arg_len(self):
        """Test that only 3 positional arguments are supported."""
        self.assertSystemExit(1, 2)
        self.assertSystemExit(1, 2, 3, 4)

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

    def test_bad_old_password(self):
        user = 'john@example.org'
        self.assertSystemExit(user, 'old pw', 'new pw')
