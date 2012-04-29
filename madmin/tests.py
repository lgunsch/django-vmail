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
        name = 'example.org'
        new_domain = Domain.objects.create(fqdn=name)
        self.assertEqual(name, str(new_domain))

        domain = Domain.objects.get(fqdn=name)
        self.assertEqual(new_domain, domain)
        self.assertEqual(name, domain.fqdn)
        self.assertIsInstance(domain.created, datetime)


class MailUserTest(TestCase):
    def test_user_profile(self):
        fqdn = 'example.org'
        name = 'john'
        password = 'johnpassword'
        salt = '12345'
        domain = Domain.objects.create(fqdn=fqdn)
        new_user = MailUser.objects.create(username=name, salt=salt,
                shadigest=password,
                domain=domain)
        self.assertEqual('john: example.org', str(new_user))

        user = MailUser.objects.get(username=name)
        self.assertEqual(new_user, user)
        self.assertEqual(name, user.username)
        self.assertEqual(salt, user.salt)
        self.assertEqual(password, user.shadigest)
        self.assertEqual(domain, user.domain)

        self.assertRaises(IntegrityError, MailUser.objects.create,
                          username=name, salt=salt,
                          shadigest=password,
                          domain=domain)

    def test_set_password(self):
        password = u'johnpassword'  # use unicode string to be like django,
        salt = u'12345'             # base64 cannot handle unicode
        domain = Domain.objects.create(fqdn='example.org')
        user = MailUser.objects.create(username='john', salt=salt,
                shadigest=password,
                domain=domain)

        user.set_password(password)

        m = hashlib.sha1()
        m.update(str(password))
        m.update(str(salt))
        hashed_password = base64.b64encode(m.digest() + str(salt))
        self.assertEqual(hashed_password, user.shadigest)

    def test_unique_username_domain(self):
        pass


class AliasTest(TestCase):
    def test_alias(self):
        domain = Domain.objects.create(fqdn='example.org')
        alias = Alias.objects.create(domain=domain, source='jonny@example.org',
                                     destination='john@example.org')
        self.assertEqual('example.org: jonny@example.org > john@example.org',
                         str(alias))