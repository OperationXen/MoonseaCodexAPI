from django.test import TestCase

from codex.models.character import Character
from codex.models.events_downtime import CatchingUp, MundaneTrade


class TestCatchUpModel(TestCase):
    """Tests for the CatchingUp downtime event model"""

    fixtures = ["test_users", "test_characters", "test_events_catchingup"]

    def test_create_catchingup(self) -> None:
        """Test that a valid catchingup event can be created"""
        char = Character.objects.get(pk=1)
        obj = CatchingUp(character=char)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, CatchingUp)
        self.assertEqual(obj.levels, 1)

    def test_delete_catchinup(self) -> None:
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


class TestMundaneTrade(TestCase):
    """Tests for the mundate trade"""

    fixtures = ["test_users", "test_characters", "test_events_mundanetrade"]

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
