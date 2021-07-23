from modules.domain import exceptions


def error(exception: Exception) -> dict:
    _err = ErrorsMap.get(exception)
    if not _err:
        _err = ErrorsMap.get(type(exception))
    return {
        "error": _err
    }


ErrorsMap = {
    exceptions.PasswordsNotMatch: "PASSWORDS_NOT_MATCH",
    exceptions.RolesUnsuitable: "ROLES_UNSUITABLE",
    exceptions.PasswordNotCompliant: "PASSWORDS_NOT_COMPLIANT",
    exceptions.InvalidToken: "INVALID_TOKEN",
    exceptions.EmailAlreadyInUse: "EMAIL_ALREADY_IN_USE",
    exceptions.AccountNotFound: "ACCOUNT_NOT_FOUND"
}
