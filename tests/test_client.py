import hmac
import hashlib
import unittest

import mock
import flexmock
import simplejson

from pinterest.client import ApiBuilder
from pinterest.client import ApiClient
from pinterest.client import CachedClientRequest
from pinterest.client import ClientRequest
from pinterest.client import cached_client


class ClientRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.client_mock = mock.Mock()
        self.requests_mock = mock.Mock()
        requests_patch = mock.patch("pinterest.client.requests",
                                    self.requests_mock)
        requests_patch.start()
        self.addCleanup(requests_patch.stop)

    def test_invoke_no_access_token(self):
        client = self.build_client(params={'value': "3", 'key': "height"})
        sig_base = client.build_sig_base()
        self.assertIsNotNone(sig_base)
        expected_base = "GET&https%3A%2F%2Fapi.pinterest.comhttp%3A%2F%2Fapi.pinterest.com%2Fv3%2Ffoo%2Fbar%2F&key=height&value=3"
        self.assertEqual(expected_base, sig_base)

    @mock.patch("pinterest.client.timestamp", mock.Mock(return_value=5678))
    def test_full_sign(self):
        self.client_mock.client_id = 1234
        self.client_mock.secret = "SECRET"
        client = self.build_client({'value': "3", 'key': "num_pins"})
        sig_base = "GET&https%3A%2F%2Fapi.pinterest.comhttp%3A%2F%2Fapi.pinterest.com%2Fv3%2Ffoo%2Fbar%2F&client_id=1234&key=num_pins&timestamp=5678&value=3"
        digest = hmac.new("SECRET", digestmod=hashlib.sha256)
        digest.update(sig_base)
        expected_sig = digest.hexdigest()
        client.sign()
        self.assertEqual(expected_sig, client.params['oauth_signature'])

    def build_client(self, params=None):
        method = "GET"
        uri = "http://api.pinterest.com/v3/foo/bar/"
        return ClientRequest(self.client_mock, method, uri, params)


class ApiBuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.client_mock = flexmock.flexmock(is_authorized=False)
        self.builder = ApiBuilder(["users"], self.client_mock)

    def test_simple_chain(self):
        builder = self.builder.foo.bar.baz
        self.assertEqual(["users", "foo", "bar", "baz"], builder.uri)

    def test_chain_with_args(self):
        builder = self.builder("me").hello(32)
        self.assertEqual(["users", "me", "hello", "32"], builder.uri)

    def test_kicker(self):
        builder = self.builder("me").get
        self.assertTrue(builder.invokable)
        self.assertEqual("GET", builder.method)

    def test_invoke(self):
        invoke = flexmock.flexmock()
        invoke.should_receive("invoke").once()
        (self.client_mock.should_receive("build_request")
         .with_args("GET", "/v3/users/me/", {})
         .and_return(invoke))
        self.builder.me.get()

    def test_invoke_with_kwargs(self):
        invoke = flexmock.flexmock()
        invoke.should_receive("invoke").once()
        (self.client_mock.should_receive("build_request")
         .with_args(
            "GET", "/v3/users/me/", {'offset': 3, 'limit': 27})
         .and_return(invoke))
        self.builder.me.get(offset=3, limit=27)


class ApiClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ApiClient(1234, "SECRET")

    def test_client_request(self):
        builder = self.client.users
        self.assertIsNotNone(builder)
        self.assertEqual(['users'], builder.uri)
        self.assertFalse(builder.invokable)
        self.assertEqual(self.client, builder.client)

    def test_build_request(self):
        request_builder_mock = mock.Mock()
        self.client.request_builder = request_builder_mock
        self.client.users('me').get()
        self.assertTrue(request_builder_mock.called)
        request_builder_mock.assert_called_once_with(
            self.client, "GET", "/v3/users/me/", {})


class CachedClientTestCase(unittest.TestCase):
    def setUp(self):
        self.response_mock = mock.Mock()

        self.requests_mock = mock.Mock(return_value=self.response_mock)
        requests_patch = mock.patch("pinterest.client.requests.get",
                                    self.requests_mock)
        requests_patch.start()
        self.addCleanup(requests_patch.stop)
        self.client = cached_client(1234, "SECRET")
        self.set_response_data({})

    def test_caching(self):
        self.client.users("me").get()
        self.set_response_data("Hello!")
        self.client.users("me").get()
        self.assertEqual(1, self.requests_mock.call_count)

    def test_clear_caching(self):
        rsp, _ = self.client.users("me").get()
        self.set_response_data("Hello!")
        CachedClientRequest.clear()
        cached_response, _ = self.client.users("me").get()
        self.assertEqual(u"Hello!", cached_response)

    def set_response_data(self, data):
        self.response_mock.content = simplejson.dumps({'code': 0, 'data': data})

