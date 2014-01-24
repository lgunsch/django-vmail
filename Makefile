all: test

test:
	@python manage.py test vmail

test-postgres:
	@echo 'Using database "vmail_test_db" and user "vmail_test" (must have create database privileges).'
	@python manage.py test vmail --settings=test_postgres_settings

.PHONY: test test-postgres
