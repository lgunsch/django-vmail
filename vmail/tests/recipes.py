"""
Model mommy recepis used for testing.
"""

from model_mommy.recipe import Recipe, foreign_key, seq

from ..models import Domain, MailUser, Alias

domain = Recipe(Domain,
                fqdn=seq('example.org'))

mailuser = Recipe(MailUser,
                  domain=foreign_key(domain),
                  username=seq('johnsmith'))

alias = Recipe(Alias,
               domain=foreign_key(domain),
               source=seq('source@example.org'),
               destination=seq('destination@example.org'))
