from django.test import TestCase

from codex.models.character import Character
from codex.models.events_downtime import FreeForm


class TestFreeformModel(TestCase):
    """Tests for the FreeForm downtime event model"""

    fixtures = ["test_users", "test_characters", "test_events_dt_freeform"]

    def test_create_freeform(self) -> None:
        """Test that a valid FreeForm event can be created"""
        char = Character.objects.get(pk=1)
        obj = FreeForm(character=char, title="Test", details="Pew pew pew")

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, FreeForm)
        self.assertEqual(obj.title, "Test")
        self.assertEqual(obj.details, "Pew pew pew")

    def test_delete_freeform(self) -> None:
        """Check that a FreeForm event can be deleted"""
        obj = FreeForm.objects.get(pk=1)

        self.assertIsInstance(obj, FreeForm)
        try:
            obj.delete()
        except:
            self.fail("Unable to delete FreeForm event")

    def test_text_representation(self) -> None:
        """Check that a FreeForm event can be represented as a string"""
        obj = FreeForm.objects.get(pk=1)
        str_rep = str(obj)

        self.assertIn(obj.character.name, str_rep)
