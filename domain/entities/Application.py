import os
import logging
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta

from domain import repository  # Repository pattern
from domain.entities import Policies

from typing import List, Dict, Any, Optional


def uuid_id() -> str:
    return str(uuid4())


def current_datetime_str() -> str:
    return datetime.now(timezone.utc).isoformat()


class ApplicationNotFound(Exception):
    pass


@dataclass
class Resource:
    object_name: str = field(default=None)
    is_used: bool = field(default=False)
    description: str = field(default=None)


@dataclass
class VersionsControl:
    pass


@dataclass
class AccountWithPolicies:
    account_id: str = field(default=None)
    project: Policies.Project = field(default=None)
    pages: Policies.Pages = field(default=None)
    items: Policies.Items = field(default=None)
    media: Policies.Media = field(default=None)
    users: Policies.Users = field(default=None)


@dataclass
class Project:
    application_id: str = field(default_factory=uuid_id)
    entity_created_date: str = field(default_factory=current_datetime_str)
    resources: Dict[str, Resource] = field(default=None)
    versions_control: VersionsControl = field(default=None)
    authorized_accounts: List[AccountWithPolicies] = field(default=None)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, source: dict) -> "Project":
        return Project(
            application_id=source.get("application_id"),
            resources={
                resource_id: Resource(**resource_data)
                for resource_id, resource_data in source.get("resources").items()
            },
            versions_control=VersionsControl(**source.get("versions_control")),
            authorized_accounts=[
                AccountWithPolicies(
                    account_id=account_policies.get("account_id"),
                    project=Policies.Project(**account_policies.get("project")),
                    pages=Policies.Pages(**account_policies.get("pages")),
                    items=Policies.Items(**account_policies.get("items")),
                    media=Policies.Media(**account_policies.get("media")),
                    users=Policies.Users(**account_policies.get("users"))
                ) for account_policies in source.get("authorized_accounts")
            ],
        )

    def create_application(self):
        repository.create_application(self.to_dict())

    def delete_application(self):
        repository.delete_application_by_id(self.application_id)

    @classmethod
    def get_application_by_id(cls, account_id: str) -> Optional["Project"]:
        found_application = repository.get_application_by_id(account_id)
        if not found_application:
            return None
        return cls.from_dict(found_application)
