import pinterest.search as search
import unittest

from tests.models.factories import QueryFactory
from tests.models.factories import UserFactory
from tests.models.mock_models import MockClient
from pinterest.models.model import Model


class SearchTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client

    def test_search_boards(self):
        search.boards(QueryFactory.attributes()['query'])
        self.assertEqual(True, self.client.called)
        self.assert_path_called(['boards', 'get'])

    def test_search_pins(self):
        search.pins(QueryFactory.attributes()['query'])
        self.assertEqual(True, self.client.called)
        self.assert_path_called(['pins', 'get'])

    def test_search_users(self):
        search.users(QueryFactory.attributes()['query'])
        self.assertEqual(True, self.client.called)
        self.assert_path_called(['users', 'get'])

    def test_search_user_pins(self):
        username = UserFactory.attributes()['username']
        search.user_pins(username, QueryFactory.attributes()['query'])
        self.assertEqual(True, self.client.called)
        self.assert_path_called(['user_pins', username, 'get'])

    def test_typeahead_suggestions(self):
        search.typeahead_suggestions(
            QueryFactory.attributes()['query'], tags='')
        self.assertEqual(True, self.client.called)
        self.assert_path_called(['typeahead', 'get'])

    def assert_path_called(self, path):
        base_path = ['search']
        base_path.extend(path)
        self.assertEqual(base_path, self.client.path_called)
