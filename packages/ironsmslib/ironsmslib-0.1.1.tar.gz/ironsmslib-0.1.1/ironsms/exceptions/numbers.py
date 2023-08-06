from .base import APIException


class NoNumbersException(APIException):
    message = "NO_NUMBERS"
    description = "no numbers at the moment"

    def __init__(self, response):
        super(NoNumbersException, self).__init__(description=self.description)
