class EmailHasAlreadyTaken(Exception):
    pass


class WrongCredentials(Exception):
    pass


class InvalidSignature(Exception):
    pass


class TransactionAlreadyHandled(Exception):
    pass
