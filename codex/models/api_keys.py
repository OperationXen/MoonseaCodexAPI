import uuid
import random
import string
from django.db import models

from codex.models.users import CodexUser

def generate_random_key():
    """ Randomly generate an API key """
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    return key


class APIKey(models.Model):
    """ An authentication token for bot access """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, help_text="Key name")
    description = models.TextField(blank=True, null=True, help_text='Description of the key usage')
    value = models.CharField(max_length=64, default=generate_random_key, help_text='Key value')

    datetime = models.DateTimeField(auto_now_add=True, help_text='When the key was created')
    user = models.ForeignKey(CodexUser, on_delete=models.CASCADE, related_name='api_keys')

    def __str__(self):
        return f"{self.name}"


    class Meta:
        verbose_name = 'API key'
        verbose_name_plural = 'API keys'
