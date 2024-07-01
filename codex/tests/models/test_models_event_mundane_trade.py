from django.test import TestCase

from codex.models.character import Character
from codex.models.events_downtime import MundaneTrade


class TestMundaneTrade(TestCase):
    """Tests for the mundate trade"""

    fixtures = ["test_users", "test_characters", "test_events_dt_mundanetrade"]

    def test_create(self):
        """Test that an instance of the model can be created"""
        char = Character.objects.get(pk=1)
        obj = MundaneTrade(character=char, purchased="Potion of healing", gold_change=50)
        self.assertIsInstance(obj, MundaneTrade)

    def test_delete(self):
        """Test that you can delete a trade event"""
        obj = MundaneTrade.objects.get(pk=1)
        self.assertIsInstance(obj, MundaneTrade)
        try:
            obj.delete()
        except:
            self.fail("Unable to delete mundanetrade event")

    def test_text_represenation(self):
        """Test that the object can be converted to a text representation"""
        obj = MundaneTrade.objects.get(pk=1)
        str_rep = str(obj)

        self.assertIn(obj.character.name, str_rep)
