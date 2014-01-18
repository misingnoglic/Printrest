class Relation(object):

    def __init__(self, finder_fn):
        self.finder_fn = finder_fn

    def __get__(self, instance, owner):
        field_name = "_%s_handler" % self.relation_name
        handler = getattr(instance, field_name, None)
        if not handler:
            handler = RelationHandler(instance, self)
            setattr(instance, field_name, handler)
        return handler

    def __repr__(self):
        return 'Relation %s' % self.relation_name

    def hook_into_model(self, model, relation_name):
        self.relation_name = relation_name
        self.model = model


class RelationHandler(object):

    def __init__(self, instance, relation):
        self.fetched = False
        self.model_instance = instance
        self.relation = relation

    def __call__(self, *args, **kwargs):
        if not self.fetched:
            param_kwargs = self.model_instance.kwargs_to_params(kwargs)
            builder = self.relation.finder_fn(self.model_instance.builder)
            data, bookmark = builder(**param_kwargs)
            self.api_data = self.model_instance.parse(
                data, bookmark, builder, param_kwargs)
            self.bookmark = bookmark
            self.fetched = True
        return self.api_data
