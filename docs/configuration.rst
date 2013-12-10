=============
Configuration
=============

Below are the **PostgreSQL** SQL queries for configuring Postfix, and Dovecot.
Note that this is **not a guide** on how to configure Postfix.  It is expected
that you have already configured Postfix.  See
`workaround.org <https://workaround.org/ispmail>`_ for a guide on configuring
a mail server.

In version 0.3.0 of django-vmail there will be commands to help you configure the
below SQL queries for your particular database.

Note: django-vmail is configured to use the SSHA password scheme with Dovecot.

Postfix
-------
These queries were tested on Postfix version 2.9 (released with Debian Wheezy), and
version 2.7 (released with Debian Squeeze).

In ``/etc/postfix/pgsql-virtual-mailbox-domains.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = SELECT 1 FROM vmail_domain WHERE vmail_domain.fqdn='%s' AND vmail_domain.active=TRUE

In ``/etc/postfix/pgsql-virtual-mailbox-maps.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = SELECT 1 \
    FROM vmail_mailuser \`
        INNER JOIN vmail_domain ON (vmail_mailuser.domain_id = vmail_domain.id) \
    WHERE vmail_mailuser.username='%u' AND \
        vmail_domain.fqdn='%d' AND \
        vmail_domain.active=TRUE AND \
        vmail_mailuser.active=TRUE

In ``/etc/postfix/pgsql-virtual-alias-maps.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = \
    SELECT vmail_alias.destination \
    FROM vmail_alias \
        INNER JOIN vmail_domain ON (vmail_alias.domain_id = vmail_domain.id) \
    WHERE vmail_alias.source = '%s' AND \
        vmail_domain.active=TRUE AND \
        vmail_alias.active=TRUE

In ``/etc/postfix/pgsql-email2email.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = \
        SELECT vmail_mailuser.username || '@' || vmail_domain.fqdn as email \
        FROM vmail_mailuser \
            INNER JOIN vmail_domain ON (vmail_mailuser.domain_id = vmail_domain.id) \
        WHERE vmail_mailuser.username = '%u' AND \
            vmail_domain.fqdn = '%d' AND \
            vmail_domain.active=TRUE AND \
            vmail_mailuser.active=TRUE

Dovecot
-------
Dovecot 1 and 2 have the same SQL query configuration, however, they may be
in diffrent file locations depending on your setup.  Dovecot 2 was shipped
with Debian Wheezy, and Dovecot 1 with Squeeze.

In ``/etc/dovecot/dovecot-sql.conf.ext`` or ``/etc/dovecot/dovecot-sql.conf``: ::

    driver = pgsql
    connect = host=127.0.0.1 dbname=<db-name> user=<db-user> password=<db-password>
    default_pass_scheme = SSHA

    password_query = \
        SELECT vmail_mailuser.username || '@' || vmail_domain.fqdn as user, vmail_mailuser.shadigest as password \
        FROM vmail_mailuser \
             INNER JOIN vmail_domain ON (vmail_mailuser.domain_id = vmail_domain.id) \
        WHERE vmail_mailuser.username = '%n' AND \
             vmail_domain.fqdn = '%d' AND \
             vmail_domain.active=TRUE AND \
             vmail_mailuser.active=TRUE

Note: You should configure Dovecot to not use user specific settings. In
the ``userdb`` section of the Dovecot configuration.  For *example* ::

    userdb {
      driver = static
      args = uid=vmail gid=vmail home=/var/vmail/%d/%n/Maildir allow_all_users=yes
    }

Helper Scripts
--------------
I have found these helper scripts useful.  Just put the following files in
``/usr/local/bin``, or somewhere else in your bin path, and make them
executable.

In ``/usr/local/bin/vmail-addmbox``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/<YOUR_VIRTUALENV_DIR>/bin/activate
    manage.py vmail-addmbox $@

In ``/usr/local/bin/vmail-addalias``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/<YOUR_VIRTUALENV_DIR>/bin/activate
    manage.py vmail-addalias $@

In ``/usr/local/bin/vmail-chpasswd``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/<YOUR_VIRTUALENV_DIR>/bin/activate
    manage.py vmail-chpasswd $@

In ``/usr/local/bin/vmail-setpasswd``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/<YOUR_VIRTUALENV_DIR>/bin/activate
    manage.py vmail-setpasswd $@
