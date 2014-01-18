import unittest

from factories import PinFactory
from mock_models import MockClient
from pinterest.models.model import Model
from pinterest.models.model import Pin


class PinTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client
        pin_data = PinFactory.attributes()
        self.pin = Pin(str(pin_data['id']))

    def test_fields_not_fetched(self):
        self.assertEqual(False, self.pin.fetched)
        try:
            pin_id = self.pin.id
        except AttributeError:
            pass
        self.assertEqual(True, self.pin.fetched)
        self.assert_path_called(['get'])

    def test_fields_fetched(self):
        self.pin.fetched = True
        attrs = PinFactory.attributes()
        self.pin.attrs = attrs
        self.assertEqual(attrs['id'], self.pin.id)
        self.client.clear_path()
        self.assertEqual(attrs['like_count'], self.pin.like_count)
        self.assertEqual(False, self.client.called)

    def test_get_comments(self):
        comments = self.pin.comments()
        self.assert_path_called(['comments', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        comments = self.pin.comments()
        self.assertEqual(False, self.client.called)

    def test_get_likes(self):
        likes = self.pin.likes()
        self.assert_path_called(['likes', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        likes = self.pin.likes()
        self.assertEqual(False, self.client.called)

    def test_get_related_boards(self):
        related_boards = self.pin.related_boards()
        self.assert_path_called(['related', 'board', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        related_boards = self.pin.related_boards()
        self.assertEqual(False, self.client.called)

    def test_get_has_related_boards(self):
        has_related_boards = self.pin.has_related_boards
        self.assert_path_called(['related', 'board_existence', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        has_related_boards = self.pin.has_related_boards
        self.assertEqual(False, self.client.called)

    def test_related_pins(self):
        related_pins = self.pin.related_pins()
        self.assert_path_called(['related', 'pin', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        related_pins = self.pin.related_pins()
        self.assertEqual(False, self.client.called)

    def test_has_related_pins(self):
        has_related_pins = self.pin.has_related_pins
        self.assert_path_called(['related', 'pin_existence', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        has_related_pins = self.pin.has_related_pins
        self.assertEqual(False, self.client.called)

    def test_repin_chain(self):
        repin_chain = self.pin.repin_chain()
        self.assert_path_called(['repinned_onto', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        repin_chain = self.pin.repin_chain()
        self.assertEqual(False, self.client.called)

    def assert_path_called(self, path, object=None):
        if not object:
            object = self.pin
        base_path = ['pins', self.pin.primary_key]
        base_path.extend(path)
        self.assertEqual(base_path, self.client.path_called)
