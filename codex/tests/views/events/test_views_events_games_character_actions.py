from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse


from codex.models.character import Character
from codex.models.events import Game


class TestCharacterGamesCharacterActionViews(TestCase):
    """Check character add / remove functionality for game events"""

    fixtures = ["test_users", "test_characters", "test_character_games"]

    def test_user_can_add_own_character_to_game(self) -> None:
        """a logged in user can add one of their characters to a game"""
        self.client.login(username="testuser2", password="testpassword")

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=3)
        test_data = {"character_uuid": character.uuid}
        self.assertNotIn(game, list(character.games.all()))

        response = self.client.post(
            reverse("game-add-character", kwargs={"uuid": game.uuid}), test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(game, list(character.games.all()))
        self.assertIn("message", response.data)

    def test_user_cannot_add_duplicate_character_to_game(self) -> None:
        """a logged in user cannot add a character to a game they are already in"""
        self.client.login(username="testuser1", password="testpassword")

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=2)
        test_data = {"character_uuid": character.uuid}
        self.assertIn(game, list(character.games.all()))

        response = self.client.post(
            reverse("game-add-character", kwargs={"uuid": game.uuid}), test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertIn(character.name, response.data["message"])

    def test_user_cannot_add_unowned_character_to_game(self) -> None:
        """a user cannot add a character they do not own to a game"""
        self.client.login(username="testuser1", password="testpassword")

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=3)
        test_data = {"character_uuid": character.uuid}
        self.assertNotIn(game, list(character.games.all()))

        response = self.client.post(
            reverse("game-add-character", kwargs={"uuid": game.uuid}), test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)
        self.assertNotIn(game, list(character.games.all()))

    def test_user_can_remove_own_character_from_game(self) -> None:
        """a logged in user can remove one of their characters from a game"""
        self.client.login(username="testuser1", password="testpassword")

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=2)
        test_data = {"character_uuid": character.uuid}
        self.assertIn(game, list(character.games.all()))

        response = self.client.post(
            reverse("game-remove-character", kwargs={"uuid": game.uuid}), test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertNotIn(game, list(character.games.all()))

    def test_user_cannot_remove_unowned_character_from_game(self) -> None:
        """A user cannot remove a character they do not own from a game"""
        self.client.login(username="testuser2", password="testpassword")

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=2)
        test_data = {"character_uuid": character.uuid}
        self.assertIn(game, list(character.games.all()))

        response = self.client.post(
            reverse("game-remove-character", kwargs={"uuid": game.uuid}), test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)
        self.assertIn(game, list(character.games.all()))
