# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Grouping'
        db.create_table('teams_grouping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inline_ordering_position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('teams', ['Grouping'])

        # Adding model 'TeamGrouping'
        db.create_table('teams_teamgrouping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inline_ordering_position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'])),
            ('grouping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Grouping'])),
        ))
        db.send_create_signal('teams', ['TeamGrouping'])


    def backwards(self, orm):
        
        # Deleting model 'Grouping'
        db.delete_table('teams_grouping')

        # Deleting model 'TeamGrouping'
        db.delete_table('teams_teamgrouping')


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
        'teams.grouping': {
            'Meta': {'ordering': "('inline_ordering_position',)", 'object_name': 'Grouping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inline_ordering_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teams.Team']", 'through': "orm['teams.TeamGrouping']", 'symmetrical': 'False'})
        },
        'teams.member': {
            'Meta': {'object_name': 'Member'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_coordinator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'teams.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'auto_join': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['teams.Member']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'teams.teamgrouping': {
            'Meta': {'ordering': "('inline_ordering_position',)", 'object_name': 'TeamGrouping'},
            'grouping': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Grouping']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inline_ordering_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"})
        }
    }

    complete_apps = ['teams']
