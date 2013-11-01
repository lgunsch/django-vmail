============================
Madmin - Mail Administration
============================

Madmin is a  Django_ app which provides a necessary framework for a
virtual domain email setup via Postfix_ and Dovecot_.

Madmin creates and manages mail domains, mailboxes, and aliases for Postfix
and Dovecot.  It allows system administrators to easily manage an email
domain database.  It is designed to work out-of-the-box with Postfix and
Dovecot, and comes pre-packaged with a set of administration commands to
accompany the default Django admin interface.

Madmin was written to work with ISP virtual mail setups, similar to the
tutorials you can find at `workaround.org`Workaround_.

Why madmin?
-----------
* You can use django-admin to quickly put together a customnized admin
  interface (rather then using phpMyAdmin, for example).
* In the spirit of Django, you can quickly put together apps to utilize
  your email database.

In The Future
-------------
* REST API for madmin.
* More admin commands.
* amavisd-new support for spamassasin configuration per mailbox.
* Mass email support.

Bugs & Feature Requests
-----------------------
Any bugs reports, or feature requests can be added to the issues_ at the github project page.

.. image:: https://d2weczhvl823v0.cloudfront.net/lgunsch/madmin/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

.. _issues: https://github.com/lgunsch/madmin/issues
.. _Workaround: https://workaround.org/ispmail
.. _Django: https://www.djangoproject.com/
.. _Dovecot: http://www.dovecot.org/
.. _Postfix: http://www.postfix.org/
