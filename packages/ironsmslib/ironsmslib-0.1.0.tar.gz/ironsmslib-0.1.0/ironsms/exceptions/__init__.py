from .limits import LimitActiveException
from .service import ServiceException
from .numbers import NoNumbersException
from .bad_key import BadKeyException
from .bad_query import BadQueryException
from .activation import ActivationFinishedException, ActivationNotExist

errors = [
    ServiceException,
    NoNumbersException,
    BadQueryException,
    BadKeyException,
    ActivationFinishedException,
    ActivationNotExist,
    LimitActiveException
]
