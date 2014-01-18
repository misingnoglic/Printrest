class Params(object):

    def __init__(self, repr_str=None):
        if not repr_str:
            self.repr = self.return_type
        else:
            self.repr = repr_str

    def __getattr__(self, item):
        return Params('%s.%s' % (self.repr, item.lower()))

    def __str__(self):
        return self.repr

    def __call__(self, *args, **kwargs):
        param_args = ['%s:%s' % (k, kwargs[k]) for k in kwargs]
        return Params('%s(%s)' % (self.repr, ','.join(param_args)))


class UserParams(Params):
    return_type = 'user'


class PinParams(Params):
    return_type = 'pin'


class BoardParams(Params):
    return_type = 'board'


class CommentParams(Params):
    return_type = 'comment'


class DomainParams(Params):
    return_type = 'domain'

user = UserParams()
pin = PinParams()
board = BoardParams()
comment = CommentParams()
domain = DomainParams()
