"""
Test the madmin models.
"""

import hashlib
import base64
from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from madmin.models import MailUser, Domain, Alias
from django.db import IntegrityError


class DomainTest(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def test_domain_string(self):
        domain = Domain.objects.get(pk=1)
        self.assertEqual(str(domain), 'example.org')
        self.assertIsInstance(domain.created, datetime)

    def test_domain_case(self):
        """Test FQDN is case-insensitive."""
        domain = Domain.objects.get(pk=1)
        upper = domain.fqdn.upper()
        self.assertRaises(IntegrityError, Domain.objects.create, fqdn=upper)

    def test_domain_set_to_lowercase(self):
        """Test FQDN is set to lowercase."""
        domain_fqdn = 'MyExampleDomain.org'
        orig_domain = Domain.objects.create(fqdn=domain_fqdn)
        domain_fqdn = domain_fqdn.lower()
        domain = Domain.objects.get(fqdn=domain_fqdn)
        self.assertEqual(orig_domain, domain)


class MailUserTest(TestCase):
    fixtures = ['madmin_model_testdata.json']

    def setUp(self):
        # use unicode string to be like django, base64 cannot handle unicode
        self.password = u'johnpassword'

    def test_user_string(self):
        user = MailUser.objects.get(pk=1)
        self.assertEqual('john@example.org', str(user))

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

    def test_username_case(self):
        """Test usename is case-insensitive."""
        user = MailUser.objects.get(pk=1)
        upper = user.username.upper()
        self.assertRaises(IntegrityError, MailUser.objects.create, username=upper, domain=user.domain)

    def test_username_set_to_lowercase(self):
        """Test username is set to lowercase."""
        username = 'MyUserName'
        domain = Domain.objects.get(pk=1)
        orig_user = MailUser.objects.create(username=username, domain=domain)
        username = username.lower()
        user = MailUser.objects.get(username=username, domain=domain)
        self.assertEqual(orig_user, user)

    def test_get_from_email(self):
        """Test get_from_email fetches MailUser correctly."""
        user = MailUser.objects.get(pk=7)
        fetched_user = MailUser.get_from_email(str(user))
        self.assertEqual(user, fetched_user)

    def test_get_from_email_bad_email(self):
        """Test a proper email is required."""
        self.assertRaises(ValidationError, MailUser.get_from_email, '')
        self.assertRaises(ValidationError, MailUser.get_from_email, '@')
        self.assertRaises(ValidationError, MailUser.get_from_email, 'a@b.c')
        self.assertRaises(ValidationError, MailUser.get_from_email, ' a@b.c ')

    def test_get_from_email_bad_domain(self):
        """Test a valid domain is required."""
        user = 'john@bad.domain.com'
        self.assertRaises(Domain.DoesNotExist, MailUser.get_from_email, user)

    def test_bad_mailuser(self):
        """Test a valid user is required."""
        user = 'bad_mailuser@example.org'
        self.assertRaises(MailUser.DoesNotExist, MailUser.get_from_email, user)


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

    def test_alias_case(self):
        """Test alias source and destination are case-insensitive."""
        alias = Alias.objects.get(pk=1)
        source_upper = alias.source.upper()
        self.assertRaises(IntegrityError, Alias.objects.create,
                          source=source_upper, destination=alias.destination,
                          domain=alias.domain)
        destination_upper = alias.destination.upper()
        self.assertRaises(IntegrityError, Alias.objects.create,
                          source=alias.source, destination=destination_upper,
                          domain=alias.domain)
        self.assertRaises(IntegrityError, Alias.objects.create,
                          source=source_upper, destination=destination_upper,
                          domain=alias.domain)

    def test_alias_set_to_lowercase(self):
        """Test source and destination are set to lowercase."""
        source = 'MySourceAddress'
        destination = 'MyDestinationAddress'
        domain = Domain.objects.get(pk=1)
        orig_alias = Alias.objects.create(source=source, destination=destination, domain=domain)
        source = source.lower()
        destination = destination.lower()
        alias = Alias.objects.get(source=source, destination=destination, domain=domain)
        self.assertEqual(orig_alias, alias)
