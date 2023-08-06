class BaseError(Exception):
    """
    Attributes:
        response_content: Response content from logic monitor
        response_status: Response status code. Basically HTTP status code
        msg: Error message
    """

    def __init__(
            self,
            response_content: str,
            response_status: int,
            msg: str
    ):
        self.response_content = response_content
        self.response_status = response_status
        self.msg = msg

    def __repr__(self):
        return f'{self.__class__.__name__}({self.msg}, resp_content={self.response_content})'


class InvalidNumOfItemsError(BaseError):
    """ Raised when the number of expected items returned from logicmonitor is not correct """
    pass


class RequestFailedError(BaseError):
    """ If return status code is not ok """
    pass


class ItemNotFoundError(BaseError):
    """ If the the item is not found on logicmonitor """
    pass
