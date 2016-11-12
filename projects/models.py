from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(default='')
    requirements = models.TextField(default='')
    timeline = models.CharField(max_length=255, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='projects')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.title)


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, related_name='positions')
    total = models.IntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.name)
