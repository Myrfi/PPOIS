class TransnationalCompanyException(Exception):
    def __init__(self, message: str, code: str = "GENERAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.code}: {self.message}"

