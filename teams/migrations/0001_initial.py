# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Team'
        db.create_table('teams_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_join', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('teams', ['Team'])


    def backwards(self, orm):
        
        # Deleting model 'Team'
        db.delete_table('teams_team')


    models = {
        'teams.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'auto_join': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['teams']
