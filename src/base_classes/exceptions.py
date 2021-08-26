class EarlyCompletionEvent(Exception):
    """Early stop due to successful completion"""

    def __init__(self, message="HTTP 200 occurred"):
        self.message = message


class SilenceEvent(EarlyCompletionEvent):
    """Early stop due to successful completion"""

    def __init__(self, message="HTTP 200 occurred"):
        self.message = message


class HTTP400Error(Exception):
    """Bad Request"""

    def __init__(self, message="HTTP error 400 occurred"):
        self.message = message


class HTTP503Error(Exception):
    """Server temporarily unavailable"""

    def __init__(self, message="HTTP error 503 occurred"):
        self.message = message


class InvalidFilterError(HTTP503Error):
    """Server temporarily unavailable"""

    def __init__(self, message="an invalid filter is used"):
        self.message = message
