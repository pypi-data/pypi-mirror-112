from .base import APIException


class LimitActiveException(APIException):
    message = "LIMIT_ACTIVE"
    description = "number activation has already been completed"
    limit: int

    def __init__(self, response):
        self.limit = response['limit']
        super(LimitActiveException, self).__init__(description=self.description)
