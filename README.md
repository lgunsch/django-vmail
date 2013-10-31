Madmin - Mail Administration
============================

Madmin is a [Django][django] app which provides the necessary framework for a
virtual domain email setup via [Postfix][postfix] and [Dovecot][dovecot].

Madmin creates and manages mail domains, mailboxes, and aliases for Postfix
and Dovecot.  It allows system administrators to easily manage an email
domain database.  It is designed to work out-of-the-box with Postfix and
Dovecot, and comes pre-packaged with a set of administration commands to
accompany the default Django admin interface.

Madmin was written to work with ISP virtual mail setups, similar to the
tutorials you can find at [Workaround.org][workaround].

Why madmin?
-----------
 * You can use django-admin to quickly put together a customnized admin interface (rather then using phpMyAdmin for example).
 * In the spirit of django, you can quickly put together apps to utilize your email database.

In The Future
-------------
* REST API for madmin.
* More admin commands.
* amavisd-new support for spamassasin configuration per mailbox.
* Mass email support.

Bugs & Feature Requests
-----------------------
Any bugs reports, or feature requests can be added to the [issue tracker][issue] at the github project page.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/lgunsch/madmin/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

[issues]: https://github.com/lgunsch/madmin/issues
[workaround]: https://workaround.org/ispmail
[django]: https://www.djangoproject.com/
[dovecot]: http://www.dovecot.org/
[postfix]: http://www.postfix.org/
