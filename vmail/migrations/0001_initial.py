# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'vmail_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'vmail', ['Domain'])

        # Adding model 'MailUser'
        db.create_table(u'vmail_mailuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.SlugField')(max_length=96)),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('shadigest', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vmail.Domain'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'vmail', ['MailUser'])

        # Adding unique constraint on 'MailUser', fields ['username', 'domain']
        db.create_unique(u'vmail_mailuser', ['username', 'domain_id'])

        # Adding model 'Alias'
        db.create_table(u'vmail_alias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vmail.Domain'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('destination', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'vmail', ['Alias'])

        # Adding unique constraint on 'Alias', fields ['source', 'destination']
        db.create_unique(u'vmail_alias', ['source', 'destination'])


    def backwards(self, orm):
        # Removing unique constraint on 'Alias', fields ['source', 'destination']
        db.delete_unique(u'vmail_alias', ['source', 'destination'])

        # Removing unique constraint on 'MailUser', fields ['username', 'domain']
        db.delete_unique(u'vmail_mailuser', ['username', 'domain_id'])

        # Deleting model 'Domain'
        db.delete_table(u'vmail_domain')

        # Deleting model 'MailUser'
        db.delete_table(u'vmail_mailuser')

        # Deleting model 'Alias'
        db.delete_table(u'vmail_alias')


    models = {
        u'vmail.alias': {
            'Meta': {'unique_together': "(('source', 'destination'),)", 'object_name': 'Alias'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vmail.Domain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'vmail.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'vmail.mailuser': {
            'Meta': {'unique_together': "(('username', 'domain'),)", 'object_name': 'MailUser'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vmail.Domain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'shadigest': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'username': ('django.db.models.fields.SlugField', [], {'max_length': '96'})
        }
    }

    complete_apps = ['vmail']