from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='projects')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.title)


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, related_name='positions')
    related_skills = models.ManyToManyField(Skill, related_name='positions')

    def __str__(self):
        return '{}'.format(self.name)
