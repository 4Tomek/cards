from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


post_save.connect(createProfile, sender=User)


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
# if user does not exist (deleting of User triggers deleting of Profile
# and this function then triggers deleting of non-existing User)


post_delete.connect(deleteUser, sender=Profile)
