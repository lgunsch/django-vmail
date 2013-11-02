=============
Configuration
=============

Below are the **PostgreSQL** SQL queries for configuring Postfix, and Dovecot.
Note that this is **not a guide** on how to configure Postfix.  It is expected
that you have already configured Postfix.  See
`workaround.org <https://workaround.org/ispmail>`_ for a guide on configuring
a mail server.

In version 0.2.0 of madmin there will be commands to help you configure the
below SQL queries for your particular database.

Note: Madmin is configured to use the SSHA password scheme with Dovecot.

Postfix
-------
These queries were tested on Postfix version 2.9, released with Debian Wheezy, and
version 2.7, released with Debian Squeeze.

In ``/etc/postfix/pgsql-virtual-mailbox-domains.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = SELECT 1 FROM madmin_domain WHERE madmin_domain.fqdn='%s' AND madmin_domain.active=TRUE

In ``/etc/postfix/pgsql-virtual-mailbox-maps.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = SELECT 1 \
    FROM madmin_mailuser \
        INNER JOIN madmin_domain ON (madmin_mailuser.domain_id = madmin_domain.id) \
    WHERE madmin_mailuser.username='%u' AND \
        madmin_domain.fqdn='%d' AND \
        madmin_domain.active=TRUE AND \
        madmin_mailuser.active=TRUE

In ``/etc/postfix/pgsql-virtual-alias-maps.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = \
    SELECT madmin_alias.destination \
    FROM madmin_alias \
        INNER JOIN madmin_domain ON (madmin_alias.domain_id = madmin_domain.id) \
    WHERE madmin_alias.source = '%s' AND \
        madmin_domain.active=TRUE AND \
        madmin_alias.active=TRUE

In ``/etc/postfix/pgsql-email2email.cf``: ::

    user = <db-user>
    password = <db-password>
    hosts = 127.0.0.1
    dbname = <db-name>

    query = \
        SELECT madmin_mailuser.username || '@' || madmin_domain.fqdn as email \
        FROM madmin_mailuser \
            INNER JOIN madmin_domain ON (madmin_mailuser.domain_id = madmin_domain.id) \
        WHERE madmin_mailuser.username = '%u' AND \
            madmin_domain.fqdn = '%d' AND \
            madmin_domain.active=TRUE AND \
            madmin_mailuser.active=TRUE

Dovecot
---------
Dovecot 1 and 2 have the same SQL query configuration, however, they may be
in diffrent file locations depending on your setup.  Dovecot 2 was shipped
with Debian Wheezy, and Dovecot 1 with Squeeze.

In ``/etc/dovecot/dovecot-sql.conf.ext`` or ``/etc/dovecot/dovecot-sql.conf``: ::

    driver = pgsql
    connect = host=127.0.0.1 dbname=<db-name> user=<db-user> password=<db-password>
    default_pass_scheme = SSHA

    password_query = \
        SELECT madmin_mailuser.username || '@' || madmin_domain.fqdn as user, madmin_mailuser.shadigest as password \
        FROM madmin_mailuser \
             INNER JOIN madmin_domain ON (madmin_mailuser.domain_id = madmin_domain.id) \
        WHERE madmin_mailuser.username = '%n' AND \
             madmin_domain.fqdn = '%d' AND \
             madmin_domain.active=TRUE AND \
             madmin_mailuser.active=TRUE

Note: You should configure Dovecot to not user specific settings. In
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

In ``/usr/local/bin/madmin-addmbox``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/helixcloud/bin/activate
    manage.py madmin-addmbox $@

In ``/usr/local/bin/madmin-addalias``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/helixcloud/bin/activate
    manage.py madmin-addalias $@

In ``/usr/local/bin/madmin-chpasswd``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/helixcloud/bin/activate
    manage.py madmin-chpasswd $@

In ``/usr/local/bin/madmin-setpasswd``: ::

    #!/bin/bash
    source /var/www/.virtualenvs/helixcloud/bin/activate
    manage.py madmin-setpasswd $@
