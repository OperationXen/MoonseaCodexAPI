from django.test import TestCase

from codex.models.character import Character
from codex.models.events_downtime import SpellbookUpdate


class TestSpellbookUpdate(TestCase):
    """Tests for a spellbook update model"""

    fixtures = ["test_users", "test_characters", "test_events_dt_mundanetrade"]

    def test_create(self):
        """Test that an instance of the model can be created"""
        char = Character.objects.get(pk=1)
        obj = SpellbookUpdate(
            character=char,
            gold=500,
            downtime=10,
        )
        self.assertIsInstance(obj, SpellbookUpdate)

    def test_delete(self):
        """Test that you can delete a spellbook update event"""
        obj = SpellbookUpdate.objects.get(pk=1)
        self.assertIsInstance(obj, SpellbookUpdate)
        try:
            obj.delete()
        except:
            self.fail("Unable to delete spellbook update event")

    def test_text_represenation(self):
        """Test that the object can be converted to a text representation"""
        obj = SpellbookUpdate.objects.get(pk=1)
        str_rep = str(obj)

        self.assertIn(obj.character.name, str_rep)
