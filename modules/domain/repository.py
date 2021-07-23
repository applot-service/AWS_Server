from modules.domain.helpers import database

from typing import Dict

_ACCOUNTS_TABLE_NAME = "Accounts"
_APPLICATIONS_TABLE_NAME = "Applications"


def get_account_by_id(account_id: str):  # Using Primary Key
    return database.get_item(_ACCOUNTS_TABLE_NAME, "account_id", account_id)


def get_account_by_email(email: str):  # Using GSI
    return database.find_item(_ACCOUNTS_TABLE_NAME, "email_index", "email", email)


def register_account(account_dict: Dict):
    return database.put_item(_ACCOUNTS_TABLE_NAME, account_dict)


def delete_account_by_id(account_id: str):
    return database.delete_item(_ACCOUNTS_TABLE_NAME, "account_id", account_id)


def edit_account_account_by_id(account_id: str):
    return database.put_item(_ACCOUNTS_TABLE_NAME, "account_id", account_id)


def get_application_by_id(application_id: str):  # Using Primary Key
    return database.get_item(_APPLICATIONS_TABLE_NAME, "application_id", application_id)


def create_application(application_dict: dict):
    return database.put_item(_APPLICATIONS_TABLE_NAME, application_dict)


def delete_application_by_id(application_id: str):
    return database.delete_item(_APPLICATIONS_TABLE_NAME, "application_id", application_id)
