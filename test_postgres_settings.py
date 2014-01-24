DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vmail_test_db',
        'USER': 'vmail_test',
        'PASSWORD': 'password',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

INSTALLED_APPS = (
    'vmail',
)

SECRET_KEY = 'abcde12345'