from django.test import TestCase

from codex.models import APIKey
from codex.models.users import CodexUser


class TestAPIKeyModel(TestCase):
    """ Tests for the APIKeys """
    fixtures = ['test_users', 'test_apikeys']

    def test_can_create_apikey(self) -> None:
        """ Test that a valid api model can be created """
        user = CodexUser.objects.get(pk=1)
        apikey = APIKey.objects.create(name='Test key', description='This is a simple key for testing', user=user)

        self.assertIsNotNone(apikey)
        self.assertIsInstance(apikey, APIKey)
        self.assertEqual(apikey.user.username, user.username)
        self.assertGreaterEqual(len(apikey.value), 64)

    def test_can_delete_apikey(self) -> None:
        """ Test that an existing apikey can be deleted """
        apikey = APIKey.objects.get(pk=1)
        self.assertIsInstance(apikey, APIKey)

        apikey.delete()
        with self.assertRaises(APIKey.DoesNotExist):
            apikey = APIKey.objects.get(pk=1)
        

    def test_apikey_string_representation(self) -> None:
        """ Ensure that the string representation includes the username """
        apikey = APIKey.objects.get(pk=1)
        string_rep = str(apikey)

        self.assertIn(apikey.name, string_rep)
        self.assertNotIn(apikey.value, string_rep)
        self.assertNotIn(str(apikey.uuid), string_rep)
