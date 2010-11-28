from django.db import models


class Team(models.Model):

    slug = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    auto_join = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
