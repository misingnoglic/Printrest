import factory

from pinterest.models.model import Board
from pinterest.models.model import Domain
from pinterest.models.model import Model
from pinterest.models.model import Pin
from pinterest.models.model import Query
from pinterest.models.model import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'annabanana{0}'.format(n))
    first_name = "Anna"
    last_name = "Banana"
    full_name = "Anna Banana"
    type = "user"


class BoardFactory(factory.Factory):
    FACTORY_FOR = Board
    id = factory.sequence(lambda n: 300000 + int(n))
    category = factory.sequence(lambda n: 'category{0}'.format(n))
    type = "board"


class PinFactory(factory.Factory):
    FACTORY_FOR = Pin
    id = factory.Sequence(lambda n: 2000000 + int(n))
    like_count = factory.Sequence(lambda n: 10 + int(n))
    repin_count = factory.Sequence(lambda n: 5 + int(n))
    type = "pin"


class DomainFactory(factory.Factory):
    FACTORY_FOR = Domain
    id = factory.Sequence(lambda n: 6000000 + int(n))
    name = factory.Sequence(lambda n: 'website{0}.com'.format(n))
    type = "domain"


class QueryFactory(factory.Factory):
    FACTORY_FOR = Query
    query = factory.Sequence(lambda n: 'query{0}'.format(n))


class ApiDataFactory(factory.Factory):
    FACTORY_FOR = Model
    id = factory.Sequence(lambda n: 2000000 + int(n))
    username = factory.Sequence(lambda n: 'person{0}'.format(n))
    url = factory.Sequence(lambda n: 'website{0}@example.com'.format(n))
    name = factory.Sequence(lambda n: 'category{0}'.format(n))
