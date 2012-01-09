# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WikiPage'
        db.create_table('knowledge_wikipage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('knowledge', ['WikiPage'])

        # Adding M2M table for field categories on 'WikiPage'
        db.create_table('knowledge_wikipage_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wikipage', models.ForeignKey(orm['knowledge.wikipage'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique('knowledge_wikipage_categories', ['wikipage_id', 'category_id'])

        # Adding M2M table for field tags on 'WikiPage'
        db.create_table('knowledge_wikipage_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wikipage', models.ForeignKey(orm['knowledge.wikipage'], null=False)),
            ('tag', models.ForeignKey(orm['taxonomy.tag'], null=False))
        ))
        db.create_unique('knowledge_wikipage_tags', ['wikipage_id', 'tag_id'])

        # Adding model 'WikiRevision'
        db.create_table('knowledge_wikirevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['knowledge.WikiPage'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('knowledge', ['WikiRevision'])

        # Adding model 'Faq'
        db.create_table('knowledge_faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('knowledge', ['Faq'])

        # Adding M2M table for field categories on 'Faq'
        db.create_table('knowledge_faq_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faq', models.ForeignKey(orm['knowledge.faq'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique('knowledge_faq_categories', ['faq_id', 'category_id'])

        # Adding M2M table for field tags on 'Faq'
        db.create_table('knowledge_faq_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faq', models.ForeignKey(orm['knowledge.faq'], null=False)),
            ('tag', models.ForeignKey(orm['taxonomy.tag'], null=False))
        ))
        db.create_unique('knowledge_faq_tags', ['faq_id', 'tag_id'])

        # Adding model 'Answer'
        db.create_table('knowledge_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['knowledge.Faq'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('knowledge', ['Answer'])

        # Adding model 'Poll'
        db.create_table('knowledge_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('knowledge', ['Poll'])

        # Adding M2M table for field categories on 'Poll'
        db.create_table('knowledge_poll_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['knowledge.poll'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique('knowledge_poll_categories', ['poll_id', 'category_id'])

        # Adding M2M table for field tags on 'Poll'
        db.create_table('knowledge_poll_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['knowledge.poll'], null=False)),
            ('tag', models.ForeignKey(orm['taxonomy.tag'], null=False))
        ))
        db.create_unique('knowledge_poll_tags', ['poll_id', 'tag_id'])

        # Adding model 'Choice'
        db.create_table('knowledge_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['knowledge.Poll'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('knowledge', ['Choice'])


    def backwards(self, orm):
        
        # Deleting model 'WikiPage'
        db.delete_table('knowledge_wikipage')

        # Removing M2M table for field categories on 'WikiPage'
        db.delete_table('knowledge_wikipage_categories')

        # Removing M2M table for field tags on 'WikiPage'
        db.delete_table('knowledge_wikipage_tags')

        # Deleting model 'WikiRevision'
        db.delete_table('knowledge_wikirevision')

        # Deleting model 'Faq'
        db.delete_table('knowledge_faq')

        # Removing M2M table for field categories on 'Faq'
        db.delete_table('knowledge_faq_categories')

        # Removing M2M table for field tags on 'Faq'
        db.delete_table('knowledge_faq_tags')

        # Deleting model 'Answer'
        db.delete_table('knowledge_answer')

        # Deleting model 'Poll'
        db.delete_table('knowledge_poll')

        # Removing M2M table for field categories on 'Poll'
        db.delete_table('knowledge_poll_categories')

        # Removing M2M table for field tags on 'Poll'
        db.delete_table('knowledge_poll_tags')

        # Deleting model 'Choice'
        db.delete_table('knowledge_choice')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'knowledge.answer': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Answer'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'answer': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['knowledge.Faq']"})
        },
        'knowledge.choice': {
            'Meta': {'ordering': "('poll', 'id')", 'object_name': 'Choice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['knowledge.Poll']"})
        },
        'knowledge.faq': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Faq'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'knowledge.poll': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Poll'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'knowledge.wikipage': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'WikiPage'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'knowledge.wikirevision': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'WikiRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['knowledge.WikiPage']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'notifications.stream': {
            'Meta': {'object_name': 'Stream'},
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_streams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['notifications.Stream']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['taxonomy.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taxonomy.tag': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taxonomy.vote': {
            'Meta': {'unique_together': "(('owner', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_votes'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['knowledge']
