============
django-vmail
============

Virtual Mail Administration
---------------------------

Django-vmail is a  Django_ app which provides a necessary framework for a
virtual domain email setup via Postfix_ and Dovecot_.

Django-vmail creates and manages virtual mail domains, mailboxes, and aliases for
Postfix and Dovecot using an SQL database (PostgreSQL).  It allows system
administrators to easily manage an email domain database.  It is designed to
work out-of-the-box with Postfix and Dovecot, and comes pre-packaged with a
set of administration commands to accompany the default Django admin
interface.

Django-vmail was written to work with ISP virtual mail setups, similar to the
tutorials you can find at `workaround.org`__.

Why django-vmail?
-----------------
* You can use django-admin to quickly put together a customized admin
  interface (rather then using phpMyAdmin, for example).
* You can use this Django app to quickly put together web apps to fully
  utilize your email database.

In The Future
-------------
* REST API for django-vmail.
* More admin commands.
* amavisd-new support for spamassasin configuration per mailbox.
* Mass email support.

Configuration
-------------
See the configuration docs_.

Bugs & Feature Requests
-----------------------
Any bugs reports, or feature requests can be added to the issue_ page at the github project.

.. image:: https://d2weczhvl823v0.cloudfront.net/lgunsch/django-vmail/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

.. _docs: https://github.com/lgunsch/django-vmail/blob/master/docs/configuration.rst
.. _issue: https://github.com/lgunsch/django-vmail/issues
.. _Workaround: https://workaround.org/ispmail
.. _Django: https://www.djangoproject.com/
.. _Dovecot: http://www.dovecot.org/
.. _Postfix: http://www.postfix.org/

__ Workaround_