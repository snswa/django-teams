from django.db import models


class Team(models.Model):

    slug = models.CharField(max_length=64)
    name = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    auto_join = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
