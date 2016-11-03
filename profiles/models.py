import uuid
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True)
    slug = models.SlugField(max_length=32, unique=True, blank=True,
                            editable=False)
    avatar = models.ImageField('Avatar picture',
                                upload_to='avatars/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)

    def save(self, *args, **kwargs):
        if self.slug is None or len(self.slug) == 0:
            self.slug = uuid.uuid4().hex
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return "{}'s profile".format(self.user.get_short_name())