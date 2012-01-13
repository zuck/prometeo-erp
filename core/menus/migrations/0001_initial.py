# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Menu'
        db.create_table('menus_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('menus', ['Menu'])

        # Adding model 'Link'
        db.create_table('menus_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', db_column='menu_id', to=orm['menus.Menu'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('new_window', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sort_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('submenu', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='parent_links', null=True, db_column='submenu_id', to=orm['menus.Menu'])),
            ('only_authenticated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('only_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('menus', ['Link'])

        # Adding M2M table for field only_with_perms on 'Link'
        db.create_table('menus_link_only_with_perms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('link', models.ForeignKey(orm['menus.link'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique('menus_link_only_with_perms', ['link_id', 'permission_id'])


    def backwards(self, orm):
        
        # Deleting model 'Menu'
        db.delete_table('menus_menu')

        # Deleting model 'Link'
        db.delete_table('menus_link')

        # Removing M2M table for field only_with_perms on 'Link'
        db.delete_table('menus_link_only_with_perms')


    models = {
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menus.link': {
            'Meta': {'ordering': "('menu', 'sort_order', 'id')", 'object_name': 'Link'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'db_column': "'menu_id'", 'to': "orm['menus.Menu']"}),
            'new_window': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'only_authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'only_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'only_with_perms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'submenu': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_links'", 'null': 'True', 'db_column': "'submenu_id'", 'to': "orm['menus.Menu']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'menus.menu': {
            'Meta': {'object_name': 'Menu'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['menus']
