class MockException(Exception):
    """Mock Exception"""

    def __init__(self, message="this is a mock exception"):
        self.message = message
