from .base import APIException


class BadQueryException(APIException):
    message = "BAD_QUERY"
    description = "incorrect parameters are specified"

    def __init__(self, response):
        super(BadQueryException, self).__init__(description=self.description)
