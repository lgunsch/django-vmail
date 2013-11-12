"""
Virtual mail administration interface configuration.
"""

from django.contrib import admin

from .models import Domain, MailUser, Alias


class DomainAdmin(admin.ModelAdmin):
    fields = ['fqdn', 'active']
    list_display = ['fqdn', 'active', 'created']
    list_filter = ['fqdn', 'active', 'created']
    search_fields = ['fqdn', 'active', 'created']
    date_hierarchy = 'created'

admin.site.register(Domain, DomainAdmin)


class MailUserAdmin(admin.ModelAdmin):
    fields = ['username', 'domain', 'active', 'shadigest', 'salt']
    list_display = ['username', 'domain', 'active', 'created']
    list_filter = ['username', 'domain', 'active', 'created']
    search_fields = ['username', 'domain__fqdn', 'active', 'created']
    date_hierarchy = 'created'

admin.site.register(MailUser, MailUserAdmin)


class AliasAdmin(admin.ModelAdmin):
    fields = ['domain', 'source', 'active', 'destination']
    list_display = ['source', 'destination', 'domain', 'active', 'created']
    list_filter = ['domain', 'active', 'created']
    search_fields = ['source', 'destination', 'domain__fqdn', 'active', 'created']
    date_hierarchy = 'created'

admin.site.register(Alias, AliasAdmin)
