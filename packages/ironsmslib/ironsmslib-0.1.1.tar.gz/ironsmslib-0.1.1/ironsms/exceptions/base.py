class APIException(Exception):
    def __init__(self, description=None, *args):
        super(APIException, self).__init__(description)
