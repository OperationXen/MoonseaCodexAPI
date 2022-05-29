from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from codex.models.dungeonmaster import DungeonMasterLog

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_dm_log(sender, instance=None, created=False, **kwargs):
    """ On user creation we create a DM log for that user """
    if created:
        DungeonMasterLog.objects.create(player=instance)
