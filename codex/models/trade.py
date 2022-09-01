from tabnanny import verbose
import uuid
from django.db import models
from django.contrib.auth import get_user_model

from codex.models.items import MagicItem
from codex.models.character import Character

user_model = get_user_model()


class Advert(models.Model):
    """ An item offered for trade """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    item = models.ForeignKey(MagicItem, null=True, on_delete=models.CASCADE, related_name='adverts')
    description = models.TextField(null=True, blank=True, help_text='Text to display on the item offered')

    def __str__(self):
        return f"{self.item.character.name} - {self.item.name}"

    class Meta:
        verbose_name = 'Trade advert'
        indexes = [
            models.Index(fields=['uuid'], name='advert_uuid_idx'),
            models.Index(fields=['item'], name='advert_item_idx')
        ]


class Offer(models.Model):
    """ Proposal of a trade """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    advert = models.ForeignKey(Advert, null=True, on_delete=models.CASCADE, related_name='proposals', help_text='Item that proposal is for')
    item = models.ForeignKey(MagicItem, null=True, on_delete=models.CASCADE, related_name='item_offers', help_text='Item offered in trade')
    description = models.TextField(null=True, blank=True, help_text='Text to display on the items offered')

    def __str__(self):    
        return f"{self.item.character.name} - {self.item.name} / {self.advert.item.name}"

    class Meta:
        verbose_name = 'Trade offer'
        indexes = [
            models.Index(fields=['uuid'], name='offer_uuid_idx'),
            models.Index(fields=['advert'], name='offer_advert_idx'),
            models.Index(fields=['item'], name='offer_item_idx')
        ]
