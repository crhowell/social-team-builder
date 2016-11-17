import uuid

from django.conf import settings
from django.db import models


def avatar_upload_path(instance, filename):
    return 'avatars/user_{}/{}'.format(instance.user.id, filename)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class UserRelatedSkill(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class UserProject(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    profile = models.ForeignKey('UserProfile', related_name='my_projects')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, related_name='profile')
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=32, unique=True, blank=True)
    has_changed_slug = models.BooleanField(default=False, editable=False)
    avatar = models.ImageField('Avatar picture',
                               upload_to=avatar_upload_path,
                               null=True,
                               blank=True)
    bio = models.TextField("Short Bio", default='')
    email_verified = models.BooleanField("Email verified", default=False)
    skills = models.ManyToManyField(Skill, through=UserRelatedSkill, blank=True, related_name='related_skills')

    @property
    def full_name(self):
        if self.first_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return '{}'.format(self.user.get_short_name())

    @property
    def get_avatar_url(self):
        print(self.avatar)
        if self.avatar:
            return '/media/{}'.format(self.avatar)

        return 'http://www.gravatar.com/avatar/{}?s=128&d=identicon'.format(
            '94d093eda664addd6e450d7e9881bcad'
        )

    def save(self, *args, **kwargs):
        # If no slug, generate random uuid.
        if not self.has_changed_slug:
            if self.slug or len(self.slug) >= 4:
                self.slug = self.slug
            else:
                self.slug = uuid.uuid4().hex
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return "{}'s profile".format(self.user.get_short_name())


class UserApplication(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='application')
    project = models.ForeignKey('projects.Project')
    position = models.ForeignKey('projects.Position')
    is_accepted = models.NullBooleanField(default=None)

    def __str__(self):
        return '{} for {}'.format(self.position, self.project)
