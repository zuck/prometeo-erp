# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Address'
        db.create_table('addressing_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='0', max_length=3)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('addressing', ['Address'])

        # Adding model 'PhoneNumber'
        db.create_table('addressing_phonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='0', max_length=3)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('addressing', ['PhoneNumber'])

        # Adding model 'SocialProfile'
        db.create_table('addressing_socialprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.CharField')(default='TW', max_length=5)),
            ('profile', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('addressing', ['SocialProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Address'
        db.delete_table('addressing_address')

        # Deleting model 'PhoneNumber'
        db.delete_table('addressing_phonenumber')

        # Deleting model 'SocialProfile'
        db.delete_table('addressing_socialprofile')


    models = {
        'addressing.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '3'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'addressing.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '3'})
        },
        'addressing.socialprofile': {
            'Meta': {'object_name': 'SocialProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'default': "'TW'", 'max_length': '5'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['addressing']
