# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('widgets_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('widgets', ['Region'])

        # Adding model 'WidgetTemplate'
        db.create_table('widgets_widgettemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('template_name', self.gf('django.db.models.fields.CharField')(default='widgets/widget.html', max_length=200, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('widgets', ['WidgetTemplate'])

        # Adding model 'Widget'
        db.create_table('widgets_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='widgets', to=orm['widgets.Region'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['widgets.WidgetTemplate'])),
            ('context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('show_title', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('widgets', ['Widget'])


    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('widgets_region')

        # Deleting model 'WidgetTemplate'
        db.delete_table('widgets_widgettemplate')

        # Deleting model 'Widget'
        db.delete_table('widgets_widget')


    models = {
        'widgets.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'widgets.widget': {
            'Meta': {'ordering': "('region', 'sort_order', 'title')", 'object_name': 'Widget'},
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widgets'", 'to': "orm['widgets.Region']"}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['widgets.WidgetTemplate']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'widgets.widgettemplate': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WidgetTemplate'},
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'template_name': ('django.db.models.fields.CharField', [], {'default': "'widgets/widget.html'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['widgets']
