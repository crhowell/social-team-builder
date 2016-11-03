from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from . import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, **kwargs):
    """As New User created, create and attach Profile"""
    print('YEEEEEEEEEEEE')
    if not kwargs.get('created'):
        return None
    profile = models.UserProfile(user=instance)
    profile.save()
