import unittest

from factories import BoardFactory
from mock_models import MockClient
from pinterest.models.model import Board
from pinterest.models.model import Model


class BoardTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        Model.client = self.client
        board_data = BoardFactory.attributes()
        self.board = Board(str(board_data['id']))

    def test_fields_not_fetched(self):
        self.assertEqual(False, self.board.fetched)
        try:
            board_id = self.board.id
        except AttributeError:
            pass
        self.assertEqual(True, self.board.fetched)
        self.assert_path_called(['get'])

    def test_fields_fetched(self):
        self.board.fetched = True
        attrs = BoardFactory.attributes()
        self.board.attrs = attrs
        self.assertEqual(attrs['id'], self.board.id)
        self.assertEqual(attrs['category'], self.board.category)
        self.assertEqual(False, self.client.called)

    def test_nonexistent_field(self):
        try:
            self.board.random_field
        except AttributeError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_get_pins(self):
        pins = self.board.pins()
        self.assert_path_called(['pins', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.board.pins()
        self.assertEqual(False, self.client.called)

    def test_get_related_boards(self):
        related_boards = self.board.related_boards()
        self.assert_path_called(['related', 'board', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.board.related_boards()
        self.assertEqual(False, self.client.called)

    def test_has_related_boards(self):
        has_related = self.board.has_related_boards
        self.assert_path_called(['related', 'board_existence', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.board.has_related_boards
        self.assertEqual(False, self.client.called)

    def test_collaborators(self):
        collaborators = self.board.collaborators()
        self.assert_path_called(['collaborators', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.board.collaborators()
        self.assertEqual(False, self.client.called)

    def test_followers(self):
        followers = self.board.followers()
        self.assert_path_called(['followers', 'get'])
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        pins = self.board.followers()
        self.assertEqual(False, self.client.called)

    def assert_path_called(self, path, object=None):
        if not object:
            object = self.board
        cmp_path = ['boards', self.board.primary_key]
        cmp_path.extend(path)
        self.assertEqual(cmp_path, self.client.path_called)
