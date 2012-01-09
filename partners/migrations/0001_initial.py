# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Contact'
        db.create_table('partners_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nickname', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ssn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='GMT', max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('main_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_of_contact', null=True, to=orm['addressing.Address'])),
            ('main_phone_number', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_of_contact', null=True, to=orm['addressing.PhoneNumber'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('partners', ['Contact'])

        # Adding M2M table for field addresses on 'Contact'
        db.create_table('partners_contact_addresses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['partners.contact'], null=False)),
            ('address', models.ForeignKey(orm['addressing.address'], null=False))
        ))
        db.create_unique('partners_contact_addresses', ['contact_id', 'address_id'])

        # Adding M2M table for field phone_numbers on 'Contact'
        db.create_table('partners_contact_phone_numbers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['partners.contact'], null=False)),
            ('phonenumber', models.ForeignKey(orm['addressing.phonenumber'], null=False))
        ))
        db.create_unique('partners_contact_phone_numbers', ['contact_id', 'phonenumber_id'])

        # Adding M2M table for field social_profiles on 'Contact'
        db.create_table('partners_contact_social_profiles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['partners.contact'], null=False)),
            ('socialprofile', models.ForeignKey(orm['addressing.socialprofile'], null=False))
        ))
        db.create_unique('partners_contact_social_profiles', ['contact_id', 'socialprofile_id'])

        # Adding M2M table for field categories on 'Contact'
        db.create_table('partners_contact_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['partners.contact'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique('partners_contact_categories', ['contact_id', 'category_id'])

        # Adding M2M table for field tags on 'Contact'
        db.create_table('partners_contact_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['partners.contact'], null=False)),
            ('tag', models.ForeignKey(orm['taxonomy.tag'], null=False))
        ))
        db.create_unique('partners_contact_tags', ['contact_id', 'tag_id'])

        # Adding model 'Partner'
        db.create_table('partners_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('is_managed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_customer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_supplier', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lead_status', self.gf('django.db.models.fields.CharField')(default='FIRST', max_length=10, null=True, blank=True)),
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True, blank=True)),
            ('ssn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='EUR', max_length=3, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='GMT', max_length=20, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('main_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_of_partner', null=True, to=orm['addressing.Address'])),
            ('main_phone_number', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_of_partner', null=True, to=orm['addressing.PhoneNumber'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('terms_of_payment', self.gf('django.db.models.fields.CharField')(default='30', max_length=100)),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assigned_partners', null=True, to=orm['auth.User'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_partners', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dashboard', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.Region'], unique=True, null=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('partners', ['Partner'])

        # Adding M2M table for field addresses on 'Partner'
        db.create_table('partners_partner_addresses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False)),
            ('address', models.ForeignKey(orm['addressing.address'], null=False))
        ))
        db.create_unique('partners_partner_addresses', ['partner_id', 'address_id'])

        # Adding M2M table for field phone_numbers on 'Partner'
        db.create_table('partners_partner_phone_numbers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False)),
            ('phonenumber', models.ForeignKey(orm['addressing.phonenumber'], null=False))
        ))
        db.create_unique('partners_partner_phone_numbers', ['partner_id', 'phonenumber_id'])

        # Adding M2M table for field social_profiles on 'Partner'
        db.create_table('partners_partner_social_profiles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False)),
            ('socialprofile', models.ForeignKey(orm['addressing.socialprofile'], null=False))
        ))
        db.create_unique('partners_partner_social_profiles', ['partner_id', 'socialprofile_id'])

        # Adding M2M table for field categories on 'Partner'
        db.create_table('partners_partner_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique('partners_partner_categories', ['partner_id', 'category_id'])

        # Adding M2M table for field tags on 'Partner'
        db.create_table('partners_partner_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False)),
            ('tag', models.ForeignKey(orm['taxonomy.tag'], null=False))
        ))
        db.create_unique('partners_partner_tags', ['partner_id', 'tag_id'])

        # Adding model 'Job'
        db.create_table('partners_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partners.Contact'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partners.Partner'])),
            ('role', self.gf('django.db.models.fields.CharField')(default='EMPLOYEE', max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('partners', ['Job'])

        # Adding model 'Letter'
        db.create_table('partners_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partners.Partner'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='target_of_letters', null=True, to=orm['partners.Contact'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('target_ref_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('target_ref_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('partners', ['Letter'])


    def backwards(self, orm):
        
        # Deleting model 'Contact'
        db.delete_table('partners_contact')

        # Removing M2M table for field addresses on 'Contact'
        db.delete_table('partners_contact_addresses')

        # Removing M2M table for field phone_numbers on 'Contact'
        db.delete_table('partners_contact_phone_numbers')

        # Removing M2M table for field social_profiles on 'Contact'
        db.delete_table('partners_contact_social_profiles')

        # Removing M2M table for field categories on 'Contact'
        db.delete_table('partners_contact_categories')

        # Removing M2M table for field tags on 'Contact'
        db.delete_table('partners_contact_tags')

        # Deleting model 'Partner'
        db.delete_table('partners_partner')

        # Removing M2M table for field addresses on 'Partner'
        db.delete_table('partners_partner_addresses')

        # Removing M2M table for field phone_numbers on 'Partner'
        db.delete_table('partners_partner_phone_numbers')

        # Removing M2M table for field social_profiles on 'Partner'
        db.delete_table('partners_partner_social_profiles')

        # Removing M2M table for field categories on 'Partner'
        db.delete_table('partners_partner_categories')

        # Removing M2M table for field tags on 'Partner'
        db.delete_table('partners_partner_tags')

        # Deleting model 'Job'
        db.delete_table('partners_job')

        # Deleting model 'Letter'
        db.delete_table('partners_letter')


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
        },
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
        'notifications.stream': {
            'Meta': {'object_name': 'Stream'},
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_streams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['notifications.Stream']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'partners.contact': {
            'Meta': {'object_name': 'Contact'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.Address']", 'null': 'True', 'blank': 'True'}),
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'main_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_of_contact'", 'null': 'True', 'to': "orm['addressing.Address']"}),
            'main_phone_number': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_of_contact'", 'null': 'True', 'to': "orm['addressing.PhoneNumber']"}),
            'nickname': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.PhoneNumber']", 'null': 'True', 'blank': 'True'}),
            'social_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.SocialProfile']", 'null': 'True', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'GMT'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'partners.job': {
            'Meta': {'object_name': 'Job'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Partner']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'EMPLOYEE'", 'max_length': '30'})
        },
        'partners.letter': {
            'Meta': {'object_name': 'Letter'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Partner']"}),
            'target_ref_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'target_ref_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target_of_letters'", 'null': 'True', 'to': "orm['partners.Contact']"})
        },
        'partners.partner': {
            'Meta': {'object_name': 'Partner'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.Address']", 'null': 'True', 'blank': 'True'}),
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assigned_partners'", 'null': 'True', 'to': "orm['auth.User']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_partners'", 'to': "orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['partners.Contact']", 'null': 'True', 'through': "orm['partners.Job']", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'dashboard': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['widgets.Region']", 'unique': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_customer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_managed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_supplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'default': "'FIRST'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'main_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_of_partner'", 'null': 'True', 'to': "orm['addressing.Address']"}),
            'main_phone_number': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_of_partner'", 'null': 'True', 'to': "orm['addressing.PhoneNumber']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.PhoneNumber']", 'null': 'True', 'blank': 'True'}),
            'social_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressing.SocialProfile']", 'null': 'True', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'}),
            'terms_of_payment': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'GMT'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
        'widgets.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['partners']
