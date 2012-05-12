"""
Test the madmin models.
"""

import hashlib
import base64
from datetime import datetime
from django.test import TestCase
from madmin.models import MailUser, Domain, Alias
from django.contrib.auth.models import User
from django.db import IntegrityError

class DomainTest(TestCase):
    def test_domain_name(self):
        """Test Domain creation."""
        name = 'example.org'
        new_domain = Domain.objects.create(fqdn=name)
        self.assertEqual(name, str(new_domain))

        domain = Domain.objects.get(fqdn=name)
        self.assertEqual(new_domain, domain)
        self.assertEqual(name, domain.fqdn)
        self.assertIsInstance(domain.created, datetime)


class MailUserTest(TestCase):
    def test_user_profile(self):
        """Test MailUser creation."""
        fqdn = 'example.org'
        name = 'john'
        domain = Domain.objects.create(fqdn=fqdn)
        new_user = MailUser.objects.create(username=name, domain=domain)
        self.assertEqual('john: example.org', str(new_user))

        user = MailUser.objects.get(username=name)
        self.assertEqual(new_user, user)
        self.assertEqual(name, user.username)
        self.assertEqual(domain, user.domain)

    def test_set_password(self):
        """Test set_password builds SSHA format password for dovecot auth."""
        # use unicode string to be like django, base64 cannot handle unicode
        password = u'johnpassword'
        domain = Domain.objects.create(fqdn='example.org')
        user = MailUser.objects.create(username='john', domain=domain)

        user.set_password(password)
        self.assertEqual(60, len(user.salt))
        salt = user.salt

        m = hashlib.sha1()
        m.update(str(password))
        m.update(str(salt))
        hashed_password = base64.b64encode(m.digest() + str(salt))
        self.assertEqual(hashed_password, user.shadigest)

    def test_unique_username_domain(self):
        """Test MailUser username-domain is unique."""
        name = 'john'
        domain = Domain.objects.create(fqdn='example.org')
        user = MailUser.objects.create(username=name, domain=domain)
        self.assertRaises(IntegrityError, MailUser.objects.create,
                          username=name, domain=domain)

        domain2 = Domain.objects.create(fqdn='example.com')
        user = MailUser.objects.create(username=name, domain=domain2)


class AliasTest(TestCase):
    def test_alias(self):
        """Test Alias creation."""
        domain = Domain.objects.create(fqdn='example.org')
        alias = Alias.objects.create(domain=domain, source='jonny@example.org',
                                     destination='john@example.org')
        self.assertEqual('example.org: jonny@example.org > john@example.org',
                         str(alias))

    def test_unique_source_destination(self):
        """Test Alias source-destination is unique."""
        domain = Domain.objects.create(fqdn='example.org')
        alias = Alias.objects.create(domain=domain, source='jonny@example.org',
                                     destination='john@example.org')
        self.assertRaises(IntegrityError, Alias.objects.create, domain=domain,
                          source='jonny@example.org',
                          destination='john@example.org')
