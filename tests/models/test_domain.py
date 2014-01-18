import unittest

from factories import DomainFactory
from pinterest.models.model import Domain
from pinterest.models.model import Model
from tests.models.mock_models import MockClient


class DomainTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client
        domain_data = DomainFactory.attributes()
        self.domain = Domain(domain_data['name'])

    def test_fields_not_fetched(self):
        self.assertEqual(False, self.domain.fetched)
        try:
            self.domain.name
        except AttributeError:
            pass
        self.assertEqual(True, self.domain.fetched)
        self.assert_path_called(['get'])

    def test_fields_fetched(self):
        self.domain.fetched = True
        attrs = DomainFactory.attributes()
        self.domain.attrs = attrs
        self.assertEqual(attrs['id'], self.domain.id)
        self.assertEqual(attrs['name'], self.domain.name)
        self.assertEqual(False, self.client.called)

    def test_nonexistent_field(self):
        try:
            self.domain.random_field
        except AttributeError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_get_pins(self):
        self.domain.pins()
        self.assert_path_called(['pins', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        self.domain.pins()
        self.assertEqual(False, self.client.called)

    def assert_path_called(self, path, object=None):
        if not object:
            object = self.domain
        base_path = ['domains', self.domain.primary_key]
        base_path.extend(path)
        self.assertEqual(base_path, self.client.path_called)
