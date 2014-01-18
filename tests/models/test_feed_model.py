import unittest

from tests.models.mock_models import MockClient
from pinterest.models.model import Feed
from pinterest.models.model import Model


class FeedTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        self.categories = [
            'animals', 'architecture', 'art', 'cars_motorcycles', 'celebrities',
            'design', 'diy_crafts', 'education', 'film_music_books', 'food_drink',
            'for_dad', 'gardening', 'geek', 'hair_beauty', 'health_fitness', 'history',
            'holidays_events', 'home_decor', 'humor', 'illustrations_posters', 'kids',
            'mens_fashion', 'outdoors', 'photography', 'products', 'quotes', 'science_nature',
            'sports', 'tattoos', 'technology', 'travel', 'weddings', 'womens_fashion']
        Model.client = self.client

    def test_get_everything_feed(self):
        self.feed = Feed('everything')
        self.client.clear_path()
        self.feed.pins()
        self.assert_path_called()
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        self.feed.pins()
        self.assertEqual(False, self.client.called)

    def test_get_category_feed(self):
        for category in self.categories:
            self.feed = Feed(category)
            self.client.clear_path()
            self.feed.pins()
            self.assert_path_called()
            self.assertEqual(True, self.client.called)
            self.client.clear_path()
            self.feed.pins()
            self.assertEqual(False, self.client.called)

    def test_get_gifts_feed(self):
        self.feed = Feed('gifts')
        self.client.clear_path()
        self.feed.pins()
        self.assert_path_called()
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        self.feed.pins()
        self.assertEqual(False, self.client.called)

    def test_get_popular_feed(self):
        self.feed = Feed('popular')
        self.client.clear_path()
        self.feed.pins()
        self.assert_path_called()
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        self.feed.pins()
        self.assertEqual(False, self.client.called)

    def test_get_video_feed(self):
        self.feed = Feed('video')
        self.client.clear_path()
        self.feed.pins()
        self.assert_path_called()
        self.assertEqual(True, self.client.called)
        self.client.clear_path()
        self.feed.pins()
        self.assertEqual(False, self.client.called)

    def assert_path_called(self):
        self.assertEqual(
            ['feeds', self.feed.primary_key, 'get'], self.client.path_called)
