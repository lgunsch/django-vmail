"""
madmin virtual mail administration interface configuration.
"""

from django.contrib import admin
from madmin.models import Domain, MailUser, Alias

class DomainAdmin(admin.ModelAdmin):
    fields = ['fqdn']
    list_display = ['fqdn', 'created']
    list_filter = ['fqdn', 'created']
    search_fields = ['fqdn', 'created']
    date_hierarchy = 'created'

admin.site.register(Domain, DomainAdmin)


class MailUserAdmin(admin.ModelAdmin):
    fields = ['username', 'domain', 'shadigest', 'salt']
    list_display = ['username', 'domain', 'created']
    list_filter = ['username', 'domain', 'created']
    search_fields = ['username', 'domain__fqdn', 'created']
    date_hierarchy = 'created'

admin.site.register(MailUser, MailUserAdmin)


class AliasAdmin(admin.ModelAdmin):
    fields = ['domain', 'source', 'destination']
    list_display = ['source', 'destination', 'domain', 'created']
    list_filter = ['source', 'destination', 'domain', 'created']
    search_fields = ['source', 'destination', 'domain__fqdn', 'created']
    date_hierarchy = 'created'

admin.site.register(Alias, AliasAdmin)
