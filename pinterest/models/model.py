from pinterest.client import ApiClient
from pinterest.relation import Relation


class ModelMetaClass(type):
    type_mapping = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)
        for obj_name, obj in attrs.items():
            new_cls.add_to_class(obj_name, obj)
        if name.lower() != "model":
            ModelMetaClass.type_mapping[name.lower()] = new_cls
        return new_cls

    def add_to_class(cls, obj_name, obj):
        if hasattr(obj, 'hook_into_model'):
            obj.hook_into_model(cls, obj_name)


class ContinuationList(object):

    def __init__(self, wrapped_list, bookmark=None,
                 builder=None, api_args=None):
        self.bookmark = bookmark
        self.builder = builder
        self.wrapped_list = wrapped_list
        self.api_args = api_args

    def __getitem__(self, index):
        while index > len(self.wrapped_list) and self.bookmark is not None:
            new_items = self.fetch_more()
            if new_items is not None:
                self.wrapped_list.extend(new_items.wrapped_list)
        return self.wrapped_list[index]

    def __setitem__(self, key, value):
        self.wrapped_list[key] = value

    def __len__(self):
        return len(self.wrapped_list)

    def __repr__(self):
        return 'bookmark:%s\n%s' % (self.bookmark, str(self.wrapped_list))

    def __iter__(self):
        for obj in self.wrapped_list:
            yield obj
        while self.bookmark is not None:
            new_items = self.fetch_more()
            if new_items is not None:
                self.wrapped_list.extend(new_items.wrapped_list)
                for obj in new_items:
                    yield obj

    def fetch_more(self, api_args=None):
        if api_args is None:
            api_args = self.api_args if self.api_args is not None else {}
        if self.bookmark:
            api_args['bookmark'] = self.bookmark
            api_data, bookmark = self.builder(
                **Model.kwargs_to_params(api_args))
            self.bookmark = bookmark
            return Model.parse(api_data, self.bookmark, self.builder, api_args)
        return None


class Model(object):
    BASE = "base"
    __metaclass__ = ModelMetaClass

    client = None

    def __init__(self, primary_key='', **kwargs):
        self.fetched = False
        self.primary_key = primary_key  # id is a string not an integer
        self.api_args = kwargs

    def __getattr__(self, name):
        if name.startswith("_"):
            return super(Model, self).__getattr__(name)
        if not self.fetched:
            self.fetch_data()
        attributes = getattr(self, 'attrs', None)
        if not attributes or name not in attributes:
            raise AttributeError("%s has no attribute: %s" % (
                self.__class__.name, name))
        return self.parse(attributes[name], builder=self.builder.get,
                          api_args=self.api_args)

    def fetch_data(self):
        data, bookmark = self.builder.get(
            **self.kwargs_to_params(self.api_args))
        self.attrs = data
        self.fetched = True

    @property
    def builder(self):
        return self.client

    @classmethod
    def from_api(cls, api_result_no_bookmark):
        attr = api_result_no_bookmark
        new_obj = cls(attr['id'])
        new_obj.attrs = attr
        new_obj.fetched = True
        return new_obj

    @classmethod
    def make_obj_from_type(cls, api_data):
        type_mapping = cls.__metaclass__.type_mapping
        return type_mapping[api_data['type']].from_api(api_data)

    @staticmethod
    def kwargs_to_params(api_args):
        formatted_args = {}
        for k in api_args:
            if isinstance(api_args[k], list):
                temp = ','.join(map(str, api_args[k]))
            else:
                temp = str(api_args[k])
            formatted_args[k] = temp
        return formatted_args

    @classmethod
    def parse(cls, api_data, bookmark=None, builder=None, api_args=None):
        if isinstance(api_data, dict) and 'type' in api_data:
            return cls.make_obj_from_type(api_data)
        elif isinstance(api_data, list):
            parsed_data = [cls.parse(res, bookmark, builder, api_args)
                           for res in api_data]
            return ContinuationList(parsed_data, bookmark,
                                    builder, api_args)
        else:
            return api_data

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.primary_key)


class Board(Model):
    related_boards = Relation(
        finder_fn=lambda builder: builder.related.board.get)
    _has_related_boards = Relation(
        finder_fn=lambda builder: builder.related.board_existence.get)
    collaborators = Relation(
        finder_fn=lambda builder: builder.collaborators.get)
    followers = Relation(finder_fn=lambda builder: builder.followers.get)
    pins = Relation(finder_fn=lambda builder: builder.pins.get)

    @property
    def builder(self):
        return self.client.boards(self.primary_key)

    @property
    def has_related_boards(self):
        return self._has_related_boards()


class Pin(Model):
    comments = Relation(finder_fn=lambda builder: builder.comments.get)
    likes = Relation(finder_fn=lambda builder: builder.likes.get)
    related_boards = Relation(
        finder_fn=lambda builder: builder.related.board.get)
    _has_related_boards = Relation(
        finder_fn=lambda builder: builder.related.board_existence.get)
    related_pins = Relation(finder_fn=lambda builder: builder.related.pin.get)
    _has_related_pins = Relation(
        finder_fn=lambda builder: builder.related.pin_existence.get)
    repin_chain = Relation(finder_fn=lambda builder: builder.repinned_onto.get)

    @property
    def builder(self):
        return self.client.pins(self.primary_key)

    @property
    def has_related_pins(self):
        return self._has_related_pins()

    @property
    def has_related_boards(self):
        return self._has_related_boards()


class User(Model):
    boards = Relation(finder_fn=lambda builder: builder.boards.get)
    followers = Relation(finder_fn=lambda builder: builder.followers.get)
    followees = Relation(finder_fn=lambda builder: builder.following.get)
    pins = Relation(finder_fn=lambda builder: builder.pins.get)
    liked_pins = Relation(finder_fn=lambda builder: builder.pins.liked.get)

    @property
    def builder(self):
        return self.client.users(self.primary_key)

    @classmethod
    def from_api(cls, api_result_no_bookmark):
        attr = api_result_no_bookmark
        user = cls(attr['username'])
        user.attrs = attr
        user.fetched = True
        return user


class CategoryMetaClass(ModelMetaClass):
    category = None

    def _all(self):
        if not self.category:
            self.category = Categories()
        return self.category.all_categories()

    all = property(_all)


class Categories(Model):
    __metaclass__ = CategoryMetaClass
    all_categories = Relation(finder_fn=lambda builder: builder)

    @property
    def builder(self):
        return self.client.categories.get


class Category(Model):

    @classmethod
    def from_api(cls, api_result_no_bookmark):
        attr = api_result_no_bookmark
        category = cls(attr['name'])
        category.attrs = attr
        category.fetched = True
        return category


class Comment(Model):
    pass


class Domain(Model):
    pins = Relation(finder_fn=lambda builder: builder.pins.get)

    @property
    def builder(self):
        return self.client.domains(self.primary_key)


class Feed(Model):
    pins = Relation(finder_fn=lambda builder: builder.get)

    @property
    def builder(self):
        return self.client.feeds(self.primary_key)


class Image(Model):

    def __init__(self, dict_values):
        self.attrs = dict_values


class Offsite(Model):
    safety = Relation(finder_fn=lambda builder: builder.get)

    @property
    def builder(self):
        return self.client.offsite


class Query(Model):
    pass


class Pinterest(object):
    @staticmethod
    def configure_client(client_id, client_secret):
        Model.client = ApiClient(client_id, client_secret)

    @staticmethod
    def authorize(access_token):
        if Model.client is not None:
            Model.client.authorize(access_token)
