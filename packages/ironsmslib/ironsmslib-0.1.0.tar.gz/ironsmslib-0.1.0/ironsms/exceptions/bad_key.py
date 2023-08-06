from .base import APIException


class BadKeyException(APIException):
    message = "BAD_KEY"
    description = "the wrong api key is specified"

    def __init__(self, response):
        super(BadKeyException, self).__init__(description=self.description)
