from .base import APIException


class ActivationFinishedException(APIException):
    message = "ACTIVATION_ALREADY_FINISHED"
    description = "number activation has already been completed"

    def __init__(self, response):
        super(ActivationFinishedException, self).__init__(description=self.description)


class ActivationNotExist(APIException):
    message = "NO_ACTIVATION"
    description = "this activation was not found"

    def __init__(self, response):
        super(ActivationNotExist, self).__init__(description=self.description)
