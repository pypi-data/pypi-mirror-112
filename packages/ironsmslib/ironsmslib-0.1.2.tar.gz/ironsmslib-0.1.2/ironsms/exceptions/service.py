from .base import APIException


class ServiceException(APIException):
    message = "SERVICE_ERROR"
    description = "service problems"

    def __init__(self, response):
        super(ServiceException, self).__init__(description=self.description)
