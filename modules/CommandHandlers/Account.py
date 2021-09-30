from modules.Domain.Entities import User
from modules.Domain import exceptions
from ApplotLibs.DataStructures.MessageBus.Events import Account as AccountEvents


def create_user(command):
    account = User.Account(
        first_name=command.first_name,
        last_name=command.last_name,
        company=command.company,
        email=command.email,
        password=command.password
    )
    try:
        registered_account_dict = account.register_account()
    except exceptions.EmailAlreadyInUse:
        return AccountEvents.EmailAlreadyInUse()
    return AccountEvents.Registered.from_dict(registered_account_dict)


def edit_user(command):  # TODO: implement
    pass


def delete_user(command):  # TODO: implement
    pass


def auth_user(command):
    email = command.email
    password = command.password

    try:
        account = User.Account.authenticate(email, password)
        account_dict = account.to_dict()
        account_dict["token"] = User.create_token_with(account.account_id)
    except exceptions.AccountNotFound:
        return AccountEvents.NotFound()
    return AccountEvents.SignedIn.from_dict(account_dict)
