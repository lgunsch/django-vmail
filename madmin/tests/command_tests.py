"""
Test the madmin commands.
"""

import sys
import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestChangePassword(TestCase):

    def setUp(self):
        self.cmd = 'madmin_chpasswd'

        # prevent CommandError's from printing to the console on stderr
        self.syserr = sys.stderr
        sys.stderr = StringIO.StringIO()

    def tearDown(self):
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
        """Test that only 3 positional arguments are supported."""
        self.assertSystemExit(1, 2)
        self.assertSystemExit(1, 2, 3, 4)
