# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Warehouse'
        db.create_table('stock_warehouse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partners.Partner'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['addressing.Address'], null=True, blank=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='managed_warehouses', null=True, to=orm['auth.User'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('dashboard', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.Region'], unique=True, null=True)),
            ('stream', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Stream'], unique=True, null=True)),
        ))
        db.send_create_signal('stock', ['Warehouse'])

        # Adding model 'Movement'
        db.create_table('stock_movement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin_of_movements', to=orm['stock.Warehouse'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destination_of_movements', to=orm['stock.Warehouse'])),
            ('product_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ProductEntry'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('stock', ['Movement'])

        # Adding model 'DeliveryNote'
        db.create_table('stock_deliverynote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_addressee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoice_addressee_of_delivery_notes', to=orm['partners.Partner'])),
            ('delivery_addressee', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='delivery_addressee_of_delivery_notes', null=True, to=orm['partners.Partner'])),
            ('order_ref_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('order_ref_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('means_of_delivery', self.gf('django.db.models.fields.CharField')(default='CARRIER', max_length=20)),
            ('reason_of_shipping', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('terms_of_shipping', self.gf('django.db.models.fields.CharField')(default='CPT', max_length=100)),
            ('delivery_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('goods_appearance', self.gf('django.db.models.fields.CharField')(default='BOX', max_length=20)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('stock', ['DeliveryNote'])

        # Adding M2M table for field entries on 'DeliveryNote'
        db.create_table('stock_deliverynote_entries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deliverynote', models.ForeignKey(orm['stock.deliverynote'], null=False)),
            ('productentry', models.ForeignKey(orm['products.productentry'], null=False))
        ))
        db.create_unique('stock_deliverynote_entries', ['deliverynote_id', 'productentry_id'])


    def backwards(self, orm):
        
        # Deleting model 'Warehouse'
        db.delete_table('stock_warehouse')

        # Deleting model 'Movement'
        db.delete_table('stock_movement')

        # Deleting model 'DeliveryNote'
        db.delete_table('stock_deliverynote')

        # Removing M2M table for field entries on 'DeliveryNote'
        db.delete_table('stock_deliverynote_entries')


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
        'products.product': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Product'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dashboard': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['widgets.Region']", 'unique': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ean13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_consumable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_sales_discount': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sales_currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'sales_price': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['partners.Partner']", 'null': 'True', 'through': "orm['products.Supply']", 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taxonomy.Tag']", 'null': 'True', 'blank': 'True'}),
            'uom': ('django.db.models.fields.CharField', [], {'default': "'UN'", 'max_length': '20'}),
            'uom_to_uos': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'uos': ('django.db.models.fields.CharField', [], {'default': "'UN'", 'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        'products.productentry': {
            'Meta': {'object_name': 'ProductEntry'},
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'tax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'products.supply': {
            'Meta': {'ordering': "('product', 'supplier')", 'unique_together': "(('product', 'supplier'),)", 'object_name': 'Supply'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_of_life': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'max_purchase_discount': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'minimal_quantity': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'purchase_currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'purchase_tax': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Partner']"}),
            'supply_method': ('django.db.models.fields.CharField', [], {'default': "'PUR'", 'max_length': '10'}),
            'warranty_period': ('django.db.models.fields.PositiveIntegerField', [], {'default': '730'})
        },
        'stock.deliverynote': {
            'Meta': {'object_name': 'DeliveryNote'},
            'delivery_addressee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'delivery_addressee_of_delivery_notes'", 'null': 'True', 'to': "orm['partners.Partner']"}),
            'delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['products.ProductEntry']", 'null': 'True', 'blank': 'True'}),
            'goods_appearance': ('django.db.models.fields.CharField', [], {'default': "'BOX'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_addressee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice_addressee_of_delivery_notes'", 'to': "orm['partners.Partner']"}),
            'means_of_delivery': ('django.db.models.fields.CharField', [], {'default': "'CARRIER'", 'max_length': '20'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_ref_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'order_ref_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'reason_of_shipping': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'terms_of_shipping': ('django.db.models.fields.CharField', [], {'default': "'CPT'", 'max_length': '100'})
        },
        'stock.movement': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Movement'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination_of_movements'", 'to': "orm['stock.Warehouse']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin_of_movements'", 'to': "orm['stock.Warehouse']"}),
            'product_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.ProductEntry']"})
        },
        'stock.warehouse': {
            'Meta': {'ordering': "['owner', 'name']", 'object_name': 'Warehouse'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addressing.Address']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'dashboard': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['widgets.Region']", 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_warehouses'", 'null': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Partner']"}),
            'stream': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.Stream']", 'unique': 'True', 'null': 'True'})
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

    complete_apps = ['stock']
