from factories import ApiDataFactory


class MockClient(object):
    methods = {"get", "post", "put", "delete"}

    def __init__(self, page_size=0):
        self.page_size = page_size
        self.invokable = False
        self.path_called = []
        self.called = False
        self.count = 0
        self.bookmark = '12445523452'

    def __get__(self, instance, owner):
        self.clear_path()
        return self

    def __getattr__(self, item):
        self.path_called.append(item)
        if item in self.methods:
            self.invokable = True
        return self

    def __call__(self, *args, **kwargs):
        if not self.invokable:
            self.path_called.append(args[0])
            return self
        else:
            self.called = True
            if self.page_size > 0:
                if kwargs.get('bookmark') is not None:
                    self.count += 1
                    if self.count > 3:
                        self.bookmark = None
                    return [{}] * self.page_size, self.bookmark
            return {}, None

    def clear_path(self):
        self.path_called = []
        self.invokable = False
        self.called = False


class MockApiResult(object):

    def get_one(self, obj_type):
        data = ApiDataFactory.attributes()
        mock_data = {}
        mock_data['id'] = data['id']
        mock_data['type'] = obj_type
        if obj_type == 'user':
            mock_data['username'] = data['username']
        if obj_type == 'category':
            mock_data['name'] = data['name']
        return mock_data

    def get_many(self, obj_type, num=5):
        return [self.get_one(obj_type) for x in range(num)]
