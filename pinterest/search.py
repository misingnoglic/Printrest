from pinterest.models.model import Model


def search(builder_fn, args, kwargs):
    builder = builder_fn(Model.client.search)
    data, bookmark = builder(*args, **Model.kwargs_to_params(kwargs))
    return Model.parse(data, bookmark, builder)


def boards(query, *args, **kwargs):
    kwargs['query'] = query
    return search(lambda builder: builder.boards.get, args, kwargs)


def pins(query, *args, **kwargs):
    kwargs['query'] = query
    return search(lambda builder: builder.pins.get, args, kwargs)


def users(query, *args, **kwargs):
    kwargs['query'] = query
    return search(lambda builder: builder.users.get, args, kwargs)


def user_pins(user_id, query, *args, **kwargs):
    kwargs['query'] = query
    return search(lambda builder: builder.user_pins(user_id).get, args, kwargs)


def typeahead_suggestions(query, *args, **kwargs):
    kwargs['q'] = query
    return search(lambda builder: builder.typeahead.get, args, kwargs)
