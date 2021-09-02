from modules.domain.helpers import database
from modules.domain.entities import Project

from typing import Dict

_ACCOUNTS_TABLE_NAME = "Accounts"
_PROJECTS_TABLE_NAME = "Projects"


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


def get_project_by_id(project_id: str):  # Using Primary Key
    return database.get_item(_PROJECTS_TABLE_NAME, "project_id", project_id)


def create_project(project_dict: dict):
    new_item = database.put_item(_PROJECTS_TABLE_NAME, project_dict)
    if not new_item:
        return None
    return Project.BaseProject.from_dict(new_item)


def delete_project_by_id(project_id: str):
    return database.delete_item(_PROJECTS_TABLE_NAME, "project_id", project_id)
