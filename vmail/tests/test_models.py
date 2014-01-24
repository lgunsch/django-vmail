"""
Test the virtual mail models.
"""

import hashlib
import base64

from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, TransactionTestCase

from ..models import MailUser, Domain, Alias
from . import recipes


class DomainTest(TestCase):

    def test_domain_string(self):
        domain = recipes.domain.make()
        self.assertEqual(str(domain), domain.fqdn)
        self.assertIsInstance(domain.created, datetime)

    def test_domain_case(self):
        """Test FQDN is case-insensitive."""
        domain = recipes.domain.make()
        upper = domain.fqdn.upper()
        with self.assertRaises(IntegrityError):
            Domain.objects.create(fqdn=upper)

    def test_domain_set_to_lowercase(self):
        """Test FQDN is set to lowercase."""
        domain_fqdn = 'MyExampleDomain.org'
        domain = recipes.domain.make(fqdn=domain_fqdn)
        self.assertEqual(domain.fqdn, domain_fqdn.lower())

    def test_active_by_default(self):
        """Domain is active by default, and not required."""
        domain = Domain.objects.create(fqdn='unique-domain.org')
        self.assertTrue(domain.active)


class MailUserTest(TestCase):

    def setUp(self):
        # use unicode string to be like django, base64 cannot handle unicode
        self.password = u'johnpassword'

    def test_user_string(self):
        user = recipes.mailuser.make()
        output = '{0}@{1}'.format(user.username, user.domain.fqdn)
        self.assertEqual(str(user), output)

    def test_set_password(self):
        """Test set_password builds SSHA format password for dovecot auth."""
        user = recipes.mailuser.make()

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
        user = recipes.mailuser.make()
        user.set_password(self.password)

        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password('johnpassword '))

    def test_unique_username_domain(self):
        """Test username-domain is unique together."""
        user = recipes.mailuser.make()
        with self.assertRaises(IntegrityError):
            MailUser.objects.create(username=user.username, domain=user.domain)

    def test_username_case(self):
        """Test usename is case-insensitive."""
        user = recipes.mailuser.make()
        upper = user.username.upper()
        with self.assertRaises(IntegrityError):
            MailUser.objects.create(username=upper, domain=user.domain)

    def test_username_set_to_lowercase(self):
        """Test username is set to lowercase."""
        username = 'MyUserName'
        user = recipes.mailuser.make(username=username)
        lower = username.lower()
        self.assertEqual(user.username, lower)

    def test_active_by_default(self):
        """MailUser is active by default, and not required."""
        domain = recipes.domain.make()
        user = MailUser.objects.create(domain=domain, username='username')
        self.assertTrue(user.active)

    def test_get_from_email(self):
        """Test get_from_email fetches MailUser correctly."""
        user = recipes.mailuser.make()
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
        # Make sure user domain exists
        Domain.objects.get_or_create(fqdn='example.org')
        user = 'bad_mailuser@example.org'
        self.assertRaises(MailUser.DoesNotExist, MailUser.get_from_email, user)


class AliasTest(TestCase):

    def test_alias_string(self):
        alias = recipes.alias.make()
        # 'example.org: bob@example.org > robert@example.org'
        output = '{0}: {1} > {2}'.format(alias.domain.fqdn,
                                         alias.source,
                                         alias.destination)
        self.assertEqual(str(alias), output)

    def test_unique_source_destination(self):
        """Test source-destination is unique together."""
        alias = recipes.alias.make()
        with self.assertRaises(IntegrityError):
            Alias.objects.create(domain=alias.domain,
                                 source=alias.source,
                                 destination=alias.destination)

    def test_alias_set_to_lowercase(self):
        """Test source and destination are set to lowercase."""
        source = 'MySourceAddress'
        destination = 'MyDestinationAddress'
        alias = recipes.alias.make(source=source, destination=destination)
        self.assertEqual(alias.source, source.lower())
        self.assertEqual(alias.destination, destination.lower())

    def test_active_by_default(self):
        """Alias is active by default, and not required."""
        domain = recipes.domain.make()
        alias = Alias.objects.create(domain=domain, source='source',
                                     destination='destination')
        self.assertTrue(alias.active)


class TransactionalAliasTest(TransactionTestCase):

    def _create(self, source, destination, domain):
        try:
            Alias.objects.create(source=source, destination=destination,
                                 domain=domain)
        except IntegrityError:
            transaction.rollback()
            raise

    def test_alias_case(self):
        """Test alias source and destination are case-insensitive."""
        alias = recipes.alias.make()

        source_upper = alias.source.upper()
        with self.assertRaises(IntegrityError):
            self._create(source_upper, alias.destination, alias.domain)

        destination_upper = alias.destination.upper()
        with self.assertRaises(IntegrityError):
            self._create(alias.source, destination_upper, alias.domain)

        with self.assertRaises(IntegrityError):
            self._create(source_upper, destination_upper, alias.domain)
