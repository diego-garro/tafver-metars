class MonthError(Exception):
    def __init__(
        self, message="The month to download must be earlier than actual month"
    ):
        super().__init__(message)


class YearError(Exception):
    def __init__(self, message="The year to download must be earlier than actual year"):
        super().__init__(message)
