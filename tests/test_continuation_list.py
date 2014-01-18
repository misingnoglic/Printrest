import unittest

from pinterest.models.model import ContinuationList
from pinterest.models.model import Model
from tests.models.mock_models import MockClient


class ContinuationListTest(unittest.TestCase):

    def setUp(self):
        self.page_size = 5
        self.client = MockClient(self.page_size)
        Model.client = self.client
        self.builder = self.client.get
        self.wrapped_list = [{}] * self.page_size
        self.continuation_list = ContinuationList(
            self.wrapped_list, bookmark='14234234', builder=self.builder)

    def test_length(self):
        self.assertEqual(len(self.continuation_list.wrapped_list),
                         len(self.continuation_list))

    def test_index_from_continuation_list(self):
        index = self.page_size + 1
        self.continuation_list[index]
        self.assertNotEqual(self.page_size, len(self.continuation_list))
        length = len(self.continuation_list)
        self.continuation_list[index + self.page_size]
        self.assertNotEqual(length, len(self.continuation_list))
        self.assertEqual(0, len(self.continuation_list) % self.page_size)

    def test_iteration_over_continuation_list(self):
        for item in self.continuation_list:
            self.assertEqual(0, len(self.continuation_list) % self.page_size)
        self.assertEqual(self.page_size * 3, len(self.continuation_list))
