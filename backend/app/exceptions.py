class UserAlreadyExistsException(Exception):
    pass


class PhoneNumberAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UsernameAlreadyExistsException(Exception):
    pass


class BorrowerNotFoundException(Exception):
    pass


class CannotRequestYourselfException(Exception):
    pass


class InvalidDueDateException(Exception):
    pass

class DebtRequestNotFoundException(Exception):
    pass

class UnauthorizedDebtRequestActionException(Exception):
    pass

class DebtRequestAlreadyProcessedException(Exception):
    pass