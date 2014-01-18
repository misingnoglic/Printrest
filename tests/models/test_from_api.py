import unittest

from mock_models import MockApiResult
from pinterest.models.model import Board
from pinterest.models.model import Category
from pinterest.models.model import Pin
from pinterest.models.model import User


class FromApiTestCase(unittest.TestCase):

    def setUp(self):
        self.result_generator = MockApiResult()

    def test_board_from_api(self):
        fake_data = self.result_generator.get_one('board')
        board = Board.from_api(fake_data)
        self.assertEqual(fake_data, board.attrs)
        self.assertEqual(fake_data['id'], board.primary_key)
        self.assertEqual(True, board.fetched)

    def test_pin_from_api(self):
        fake_data = self.result_generator.get_one('pin')
        pin = Pin.from_api(fake_data)
        self.assertEqual(fake_data, pin.attrs)
        self.assertEqual(fake_data['id'], pin.primary_key)
        self.assertEqual(True, pin.fetched)

    def test_user_from_api(self):
        fake_data = self.result_generator.get_one('user')
        user = User.from_api(fake_data)
        self.assertEqual(fake_data, user.attrs)
        self.assertEqual(fake_data['username'], user.primary_key)
        self.assertEqual(True, user.fetched)

    def test_category_from_api(self):
        fake_data = self.result_generator.get_one('category')
        category = Category.from_api(fake_data)
        self.assertEqual(fake_data, category.attrs)
        self.assertEqual(fake_data['name'], category.primary_key)
        self.assertEqual(True, category.fetched)
