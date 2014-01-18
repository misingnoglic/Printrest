from pinterest.client import ApiClient
from tests.models.factories import finders

class FakeRequestBuilder(object):

    def __init__(self, api_response=None, bookmark=None):
        self.method = None
        self.client = None
        self.path = None
        self.params = None
        if api_response is None:
            api_response = {}

        self.api_response = api_response
        self.bookmark = bookmark

    def build_request(self, client, method, path, params):
        self.client = client
        self.method = method
        self.path = path
        self.params = params
        return self

    def invoke(self):
        if self.api_response is not None:
            return self.api_response, self.bookmark

        path_parts = [part for part in self.path.split("/") if part][1:]

        model_type = path_parts[0]
        rest = path_parts[1:]

        if model_type == 'users':
            return self.handle_user_path(rest)
        elif model_type == 'pins':
            return self.handle_pins_path(rest)
        elif model_type == 'boards':
            return self.handle_boards_path(rest)
        else:
        return self.api_response, self.bookmark

    def to_printable_url(self):
        return "%s:%s:%s" % (self.method, self.path, self.params)

    def handle_user_path(self, path):
        user_spec = path[0]
        user = finders.user_by_id(int(user_spec))
        if len(path) == 1:
            user_dict = user._data if user else {}
            return user_dict, None

        next = path[1]
        if next == 'pins':
            pins = finders.user_pins(user)
            pin_dicts = [pin.to_dict() for pin in pins]
            return pin_dicts, None

        elif next == 'boards':
            boards = finders.user_boards(user)
            board_dicts = [board.to_dict() for board in boards]
            return board_dicts, None

    def handle_pins_path(self, path):
        pin = finders.pin_by_id(path[0])
        if len(path) == 1:
            pin_dict = pin.to_dict() if pin else {}
            return pin_dict, None

    def handle_boards_path(self, path):
        board = finders.board_by_id(path[0])
        if len(path) == 1:
            board_dict = board.to_dict() if board else {}
            return board_dict, None



def mock_client_and_builder(api_response=None, bookmark=None):
    mock_builder = FakeRequestBuilder(api_response=api_response, bookmark=bookmark)

    return ApiClient("0", "0", request_builder=mock_builder.build_request), mock_builder

