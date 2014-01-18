import unittest

from mock_models import MockClient
from pinterest.models.model import Categories
from pinterest.models.model import Model


class CategoryTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client

    def test_get_categories(self):
        self.client.clear_path()
        Categories.all
        self.assertEqual(['categories', 'get'], self.client.path_called)
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        Categories.all
        self.assertEqual(False, self.client.called)
