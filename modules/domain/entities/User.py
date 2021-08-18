import os
import logging
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

import jwt
import bcrypt

from modules.domain import repository, exceptions

from typing import List, Optional

# JWT_SECRET = os.getenv("JWT_SECRET")
JWT_SECRET = "SUPER SECRET"
JWT_ALGORITHM = "HS256"


def uuid_id() -> str:
    return str(uuid4())


def current_datetime_str() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_password_policy(password: str) -> bool:
    """
    Check if given password is compliant with the OWASP Security standards
    """

    owasp_special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    complexity_rules = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: any(x in owasp_special_characters for x in s)
    ]
    rules_score = sum([rule(password) for rule in complexity_rules])
    boolean_result = rules_score >= 3 and 10 <= len(password) <= 128

    logging.info("Password is " + "not " * (not boolean_result) + "compliant")
    return boolean_result


def create_token_with(account_id: str) -> str:
    payload = {'account_id': account_id}
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    if type(token) == bytes:
        return token.decode('utf-8')
    return token


def get_account_id_from_token(token: str) -> str:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise exceptions.InvalidToken

    return decoded_token["account_id"]


@dataclass
class ProjectInfo:
    project_id: str = field(default_factory=uuid_id)
    description: str = field(default=None)


@dataclass
class Account:
    account_id: str = field(default_factory=uuid_id)
    entity_created_date: str = field(default_factory=current_datetime_str)
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    company: str = field(default=None)
    email: str = field(default=None)
    password: str = field(default=None)
    projects: List[ProjectInfo] = field(default=None)  # IDs

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, source: dict) -> "Account":
        return cls(**source)

    def register_account(self):
        found_account = repository.get_account_by_email(self.email)
        if found_account:
            raise exceptions.EmailAlreadyInUse
        repository.register_account(self.to_dict())

    def delete_account(self):
        repository.delete_account_by_id(self.account_id)

    def edit_account(self):
        repository.edit_account_by_id(self.account_id)

    @classmethod
    def authenticate(cls, email: str, password: str) -> "Account":
        account = cls.get_account_by_email(email)
        if not account:
            raise exceptions.AccountNotFound
        if not bcrypt.checkpw(password.encode(), account.password.encode()):
            raise exceptions.AccountNotFound
        return account

    @classmethod
    def get_account_by_id(cls, account_id: str) -> Optional["Account"]:
        found_account = repository.get_account_by_id(account_id)
        if not found_account:
            return None
        return cls.from_dict(found_account)

    @classmethod
    def get_account_by_email(cls, email: str) -> Optional["Account"]:
        found_account = repository.get_account_by_email(email)
        if not found_account:
            return None
        return cls.from_dict(found_account)
