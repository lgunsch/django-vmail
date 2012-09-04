"""
madmin virtual mail administration models.
"""

import string
import random
import hashlib
import base64
from django.db import models


class Domain(models.Model):
    """Represents a virtual mail domain."""
    fqdn = models.CharField(max_length=256, unique=True,
                            help_text="Virtual mailbox domains, fully"
                                      " qualified.  Ex: 'example.org'.")
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.fqdn


class MailUser(models.Model):
    """
    Represents a virtual mail user address, also known as the left-hand-side
    or LHS.
    """
    username = models.SlugField(max_length=96,
                                help_text="Virtual mail domain user address or"
                                          " LHS.  Ex: 'johnsmith'.")
    salt = models.CharField(max_length=96, blank=True,
                            help_text='Random password salt.')
    shadigest = models.CharField(max_length=256, blank=True,
                                 help_text='Base64 encoding of SHA1 digest:'
                                           'Base64(sha1(password + salt) + salt).')
    domain = models.ForeignKey(Domain)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('username', 'domain'),)

    def _get_digest(self, raw_password, salt):
        """
        Returns a base64 encoded SHA1 digest using the provided
        raw_password and salt.  The digest is encoded using the
        following format:

        Base64(sha1(raw_password + salt) + salt)
        """
        # base64 does not work on unicode, so convert all django unicode strings
        # into normalized strings firt. Use str, since it will throw an error
        # if there are non-ascii characters
        m = hashlib.sha1()
        m.update(str(raw_password))
        m.update(str(salt))
        digest = base64.b64encode(m.digest() + str(self.salt))
        return digest

    def set_password(self, raw_password):
        """
        Sets the mail user password.  The Password is a base64 encoding
        of the SHA1 digest with the salt appended.  The SHA1 digest is
        the SHA1 of the raw password with the salt appended.  This is a
        compatible method of authentication with mail services such as
        dovecot.

        Ex: shadigest = Base64(sha1(password + salt) + salt)
        """
        # new salt, avoid whitespace
        chars = string.letters + string.digits + string.punctuation
        self.salt = ''.join(random.choice(chars) for x in xrange(60))
        self.shadigest = self._get_digest(raw_password, self.salt)

    def check_password(self, raw_password):
        """
        Returns True if the given raw string is the correct password
        for the mail user. (This takes care of the password hashing in
        making the comparison.)
        """
        digest = self._get_digest(raw_password, self.salt)
        if self.shadigest == digest:
            return True
        else:
            return False

    def __unicode__(self):
        return '%s: %s' % (self.username, self.domain.fqdn)


class Alias(models.Model):
    """
    Represents a virtual mailbox alias.  A virtual alias cannot receive
    mail, but may only forward mail to other email addresses.  The
    source address may be repeated for each destination mailbox to
    forward to, and may also forward to a mailbox of the same address
    to keep a copy of an email.  A source address may alo not have a
    name portion if the destination address is to be a catch-all mailbox.
    Source and destination addresses are not required to be local,
    and thus are not necessarily related to local virtual mailbox users.

    @example.org  >  john@example.org  # catch-all alias
    john@example.org  >  john@example.org  # keep a copy
    john@example.org  >  jeff@example.com  # forward john to jeff
    """
    domain = models.ForeignKey(Domain, help_text='Domain owning the alias.')
    source = models.CharField(max_length=256,
                              help_text='Fully qualified alias address of'
                                        ' destination address.  May be'
                                        ' non-local. Ex: john@example.org')
    destination = models.EmailField(max_length=256,
                                    help_text='Fully qualified destination '
                                              'mailbox address.  May be '
                                              'non-local. Ex: jeff@example.com.')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('source', 'destination'),)

    def __unicode__(self):
        return '%s: %s > %s' % (self.domain.fqdn, self.source, self.destination)
