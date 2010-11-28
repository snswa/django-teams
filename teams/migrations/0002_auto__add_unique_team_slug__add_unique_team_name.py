# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Team', fields ['slug']
        db.create_unique('teams_team', ['slug'])

        # Adding unique constraint on 'Team', fields ['name']
        db.create_unique('teams_team', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Team', fields ['name']
        db.delete_unique('teams_team', ['name'])

        # Removing unique constraint on 'Team', fields ['slug']
        db.delete_unique('teams_team', ['slug'])


    models = {
        'teams.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'auto_join': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['teams']
