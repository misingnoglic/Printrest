import calendar
import datetime
import hashlib
import hmac
import json
import urllib

import requests


def utf8_str(s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    elif isinstance(s, basestring):
        return s
    return str(s)


def timestamp():
    now = datetime.datetime.now()
    return int(calendar.timegm(now.timetuple()))


def raw_client(client_id, client_secret):
    return ApiClient(client_id, client_secret)


def cached_client(client_id, client_secret):
    def build_cached_request(client, method, path, params):
        return CachedClientRequest(client, method, path, params)

    return ApiClient(client_id, client_secret,
                     request_builder=build_cached_request)


def parse_response(response):
    if response['code'] == 0:
        return response['data'], response.get("bookmark")

    else:
        raise ApiError(response.get('code'),
                       response.get('message'),
                       response.get('message_detail'))


class ApiError(Exception):
    def __init__(self, code, message, detail):
        self.code = code
        self.message = message
        self.detail = detail

    def __repr__(self):
        return "<ApiError %s %s %s>" % (self.code, self.message, self.detail)


class ClientRequest(object):
    base_url = "https://api.pinterest.com"

    def __init__(self, client, method, uri, params=None):
        self.client = client
        self.method = method
        self.uri = uri
        self.params = params if params else {}

    def invoke(self):
        if 'access_token' not in self.params:
            self.sign()

        request_method = getattr(requests, self.method.lower())
        response = request_method(self.to_url(), params=self.params)
        return parse_response(json.loads(response.content))

    def to_url(self, include_params=False):
        if not include_params or not self.params:
            return self.base_url + self.uri

        param_list = ["%s=%s" % (name, value)
                      for name, value in self.params.iteritems()]
        query_string = "&".join(param_list)
        return "%s?%s" % (self.to_url(), query_string)

    def sign(self):
        self.params['client_id'] = self.client.client_id
        self.params['timestamp'] = timestamp()
        sig_string = self.build_sig_base()
        digest = hmac.new(self.client.secret, digestmod=hashlib.sha256)
        digest.update(sig_string)
        self.params['oauth_signature'] = digest.hexdigest()

    def build_sig_base(self):
        param_tuples = [(urllib.quote(utf8_str(key), safe="~"),
                         urllib.quote(utf8_str(value), safe="~"))
                        for key, value in self.params.iteritems()]
        param_tuples.sort()
        param_strings = ["%s=%s" % (key, value) for key, value in param_tuples]
        sig_parts = [
            self.method.upper(),
            urllib.quote_plus(self.to_url()),
            "&".join(param_strings)]
        sig_string = "&".join(sig_parts)
        return sig_string

class CachedClientRequest(ClientRequest):
    response_cache = {}


    class CacheEntry(object):
        def __init__(self, value, expires_at):
            self.value = value
            self.expires_at = expires_at

        @property
        def is_expired(self):
            if not self.expires_at:
                return False

            return self.expires_at < datetime.datetime.now()


    @classmethod
    def prune(cls):
        new_cache = {}
        for key, entry in cls.response_cache.iteritems():
            if not entry.is_expired():
                new_cache[key] = entry

        cls.response_cache = new_cache

    @classmethod
    def clear(cls):
        cls.response_cache.clear()

    def invoke(self):
        cache_key = self.__get_cache_key()
        results = self.response_cache.get(cache_key)

        if not results or results.is_expired:
            now = datetime.datetime.now()
            api_response = super(CachedClientRequest, self).invoke()
            results = self.CacheEntry(api_response,
                                      now + datetime.timedelta(minutes=5))
            self.response_cache[cache_key] = results

        return results.value

    def __get_cache_key(self):
        return "%s:%s" % (self.method, self.to_url(include_params=True))


class ApiBuilder(object):
    methods = {"get", "post", "put", "delete"}

    def __init__(self, base, client):
        self.uri = base
        self.method = "GET"
        self.client = client
        self.invokable = False

    def __getattr__(self, item):
        if item.lower() in self.methods:
            self.method = item.upper()
            self.invokable = True
            return self

        self.invokable = False

        return self(item, self.client)

    def __call__(self, *args, **kwargs):
        if self.invokable:
            if self.client.is_authorized:
                kwargs['access_token'] = self.client.access_token

            full_path = "/v3/%s/" % "/".join(self.uri)
            request = self.client.build_request(self.method, full_path, kwargs)
            return request.invoke()

        uri_copy = self.__copy_and_extend_uri(args[0])
        return self.__class__(uri_copy, self.client)

    def __copy_and_extend_uri(self, item):
        uri_copy = []
        uri_copy.extend(self.uri)
        uri_copy.append(str(item))
        return uri_copy


class ApiClient(object):
    def __init__(self, client_id, client_secret, request_builder=None):
        self.client_id = client_id
        self.secret = client_secret
        self.access_token = None

        def default_request_builder(client, method, path, params):
            return ClientRequest(client, method, path, params)

        self.request_builder = request_builder if request_builder else default_request_builder

    def __getattr__(self, item):
        return ApiBuilder([item], self)

    def build_request(self, method, path, params):
        return self.request_builder(self, method, path, params)

    def authorize(self, access_token):
        self.access_token = access_token

    @property
    def is_authorized(self):
        return self.access_token is not None
