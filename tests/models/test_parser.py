import unittest

from mock_models import MockApiResult, MockClient
from pinterest.models.model import Board
from pinterest.models.model import Comment
from pinterest.models.model import ContinuationList
from pinterest.models.model import Model
from pinterest.models.model import Pin
from pinterest.models.model import User


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.model = Model(primary_key='')
        Model.client = MockClient()
        self.result_generator = MockApiResult()

    def test_single_board(self):
        self.assert_type(Board, self.model.parse(
            self.result_generator.get_one('board')))

    def test_list_board(self):
        result = self.model.parse(self.result_generator.get_many('board'))
        self.assert_type(ContinuationList, result)
        for r in result:
            self.assert_type(Board, r)

    def test_single_pin(self):
        self.assert_type(Pin, self.model.parse(
            Pin, self.result_generator.get_one('pin')))

    def test_list_pin(self):
        result = self.model.parse(self.result_generator.get_many('pin'))
        self.assert_type(ContinuationList, result)
        for r in result:
            self.assert_type(Pin, r)

    def test_single_user(self):
        self.assert_type(User, self.model.parse(
            User, self.result_generator.get_one('user')))

    def test_list_user(self):
        result = self.model.parse(self.result_generator.get_many('user'))
        self.assert_type(ContinuationList, result)
        for r in result:
            self.assert_type(User, r)

    def test_single_comment(self):
        self.assert_type(Comment, self.model.parse(
            self.result_generator.get_one('comment')))

    def test_list_comments(self):
        result = self.model.parse(self.result_generator.get_many('comment'))
        self.assert_type(ContinuationList, result)
        for r in result:
            self.assert_type(Comment, r)

    def test_parse_join(self):
        api_data = self.result_generator.get_one('pin')
        api_data['pinner'] = self.result_generator.get_one('user')
        pin = Pin(api_data['id'])
        pin.attrs = api_data
        pin.fetched = True
        self.assert_type(Pin, pin)
        pinner = pin.pinner
        self.assert_type(User, pinner)

    def assert_type(self, expected_type, result):
        return isinstance(Comment, expected_type)
