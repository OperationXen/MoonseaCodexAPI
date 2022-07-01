from django.test import TestCase

from codex.models import CodexUser


class TestCodexUserModel(TestCase):
    """ Tests for the user model """
    fixtures = ['test_users']

    def test_can_create_codexuser(self) -> None:
        """ Test that a valid user model can be created """
        user = CodexUser.objects.create_user('test', 'testcreate@moonseacodex.local', 'testpassword')

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'testcreate@moonseacodex.local')

    def test_can_delete_codexuser(self) -> None:
        """ Test that an existing codexuser can be deleted """
        user = CodexUser.objects.get(username='testuser1')
        user.delete()

        with self.assertRaises(CodexUser.DoesNotExist):
            user = CodexUser.objects.get(username='testuser1')

    def test_can_add_discord_info_to_codexuser(self) -> None:
        """ Ensure that an existing user can be editted to include discord information """
        discord_name = 'discord_name#1234'

        user = CodexUser.objects.get(username='testuser1')
        self.assertNotEqual(user.discord_id, discord_name)
        user.discord_id = discord_name
        user.save()

        user = CodexUser.objects.get(username='testuser1')
        self.assertEqual(user.discord_id, discord_name)

    def test_codexuser_string_representation(self) -> None:
        """ Ensure that the string representation includes the username """
        user = CodexUser.objects.get(username='testuser1')
        string_rep = str(user)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser1')
        self.assertIn(string_rep, 'testuser1')
