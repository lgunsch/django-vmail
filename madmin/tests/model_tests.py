"""
Test the madmin models.
"""

import hashlib
import base64
from datetime import datetime
from django.test import TestCase
from madmin.models import MailUser, Domain, Alias
from django.db import IntegrityError


class DomainTest(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def test_domain_string(self):
        domain = Domain.objects.get(pk=1)
        self.assertEqual(str(domain), 'example.org')
        self.assertIsInstance(domain.created, datetime)


class MailUserTest(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def setUp(self):
        # use unicode string to be like django, base64 cannot handle unicode
        self.password = u'johnpassword'

    def test_user_string(self):
        user = MailUser.objects.get(pk=1)
        self.assertEqual('john: example.org', str(user))

    def test_set_password(self):
        """Test set_password builds SSHA format password for dovecot auth."""
        user = MailUser.objects.get(pk=1)

        user.set_password(self.password)
        self.assertEqual(user.SALT_LEN, len(user.salt))
        salt = user.salt

        m = hashlib.sha1()
        m.update(str(self.password))
        m.update(str(salt))
        hashed_password = base64.b64encode(m.digest() + str(salt))
        self.assertEqual(hashed_password, user.shadigest)

    def test_check_password(self):
        """Test check_password returns correct results for a mail user."""
        user = MailUser.objects.get(pk=1)
        user.set_password(self.password)

        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password('johnpassword '))

    def test_unique_username_domain(self):
        """Test username-domain is unique together."""
        user = MailUser.objects.get(pk=1)
        self.assertRaises(IntegrityError, MailUser.objects.create,
                          username=user.username, domain=user.domain)


class AliasTest(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def test_alias_string(self):
        alias = Alias.objects.get(pk=1)
        self.assertEqual('example.org: bob@example.org > robert@example.org',
                         str(alias))

    def test_unique_source_destination(self):
        """Test source-destination is unique together."""
        alias = Alias.objects.get(pk=1)
        self.assertRaises(IntegrityError, Alias.objects.create,
                          domain=alias.domain,
                          source=alias.source,
                          destination=alias.destination)
