import copy


class OptimusException(Exception):
    pass


class ConnectionException(OptimusException):
    """
    An exception that occurs when the Optimus was unavailable.
    """

    def __init__(self, message):
        super(ConnectionException, self).__init__(message)
        self.message = message

    def __str__(self):
        return f"ConnectionException: {self.message if self.message is not None else ''}"


class ApiException(OptimusException):
    """An exception that occurs when the Optimus API was contacted successfully,
    but it responded with an error.
    """

    def __init__(self, response, status_code):
        self.message = response.get("message", None) if response is not None else None
        self.message = self.message if self.message != "" else response.get("error", None)
        self.x_request_id = response.get("x-request-id", "")
        self._body = response
        if self.message is not None:
            super(ApiException, self).__init__(self.message)
        else:
            super(ApiException, self).__init__()
        self.status_code = status_code

    def __str__(self):
        return f"ApiException: status: {self.status_code}, x-request-id: {self.x_request_id}, " \
               f"{self.message if self.message is not None else ''}"

    def to_json(self):
        return copy.deepcopy(self._body)


class SchemasException(OptimusException):
    """
    An exception that occurs when Optimus' schemas with an error.
    """

    def __init__(self, message):
        super(SchemasException, self).__init__()
        self.message = message

    def __str__(self):
        return f"SchemasException: {self.message if self.message is not None else ''}"
