import unittest

from factories import UserFactory
from mock_models import MockClient
from pinterest.models.model import Model
from pinterest.models.model import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client
        user_data = UserFactory.attributes()
        self.user = User(user_data['username'])

    def test_fields_not_fetched(self):
        self.assertEqual(False, self.user.fetched)
        try:
            username = self.user.username
        except AttributeError:
            pass
        self.assertEqual(True, self.user.fetched)
        self.assert_path_called(['get'])

    def test_fields_fetched(self):
        self.user.fetched = True
        attrs = UserFactory.attributes()
        self.user.attrs = attrs
        self.assertEqual(attrs['username'], self.user.username)
        self.client.clear_path()
        self.assertEqual(attrs['first_name'], self.user.first_name)
        self.assertEqual(False, self.client.called)

    def test_get_boards(self):
        boards = self.user.boards()
        self.assert_path_called(['boards', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        boards = self.user.boards()
        self.assertEqual(False, self.client.called)

    def test_get_followers(self):
        followers = self.user.followers()
        self.assert_path_called(['followers', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        followers = self.user.followers()
        self.assertEqual(False, self.client.called)

    def test_get_followees(self):
        followees = self.user.followees()
        self.assert_path_called(['following', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        followees = self.user.followees()
        self.assertEqual(False, self.client.called)

    def test_get_pins(self):
        pins = self.user.pins()
        self.assert_path_called(['pins', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.user.pins()
        self.assertEqual(False, self.client.called)

    def test_get_liked_pins(self):
        liked_pins = self.user.liked_pins()
        self.assert_path_called(['pins', 'liked', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        liked_pins = self.user.liked_pins()
        self.assertEqual(False, self.client.called)

    def assert_path_called(self, path, object=None):
        if not object:
            object = self.user
        base_path = ['users', self.user.primary_key]
        base_path.extend(path)
        self.assertEqual(base_path, self.client.path_called)
