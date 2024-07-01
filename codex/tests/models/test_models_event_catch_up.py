from django.test import TestCase

from codex.models.character import Character
from codex.models.events_downtime import CatchingUp, MundaneTrade


class TestCatchUpModel(TestCase):
    """Tests for the CatchingUp downtime event model"""

    fixtures = ["test_users", "test_characters", "test_events_dt_catchingup"]

    def test_create_catchingup(self) -> None:
        """Test that a valid catchingup event can be created"""
        char = Character.objects.get(pk=1)
        obj = CatchingUp(character=char)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, CatchingUp)
        self.assertEqual(obj.levels, 1)

    def test_delete_catchingup(self) -> None:
        """Check that a CatchingUp event can be deleted"""
        obj = CatchingUp.objects.get(pk=1)

        self.assertIsInstance(obj, CatchingUp)
        try:
            obj.delete()
        except:
            self.fail("Unable to delete CatchingUp event")

    def test_text_representation(self) -> None:
        """Check that a CatchingUp event can be represented as a string"""
        obj = CatchingUp.objects.get(pk=1)
        str_rep = str(obj)

        self.assertIn(obj.character.name, str_rep)
