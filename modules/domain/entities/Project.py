from uuid import uuid4
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

from modules.domain import repository
from modules.domain.entities import Policies

from typing import List, Dict, Optional


def uuid_id() -> str:
    return str(uuid4())


def current_datetime_str() -> str:
    return datetime.now(timezone.utc).isoformat()


class ProjectNotFound(Exception):
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
class BaseProject:
    project_id: str = field(default_factory=uuid_id)
    title: str = field(default=None)
    description: str = field(default=None)
    last_updated: str = field(default=None)
    entity_created_date: str = field(default_factory=current_datetime_str)
    resources: Dict[str, Resource] = field(default=None)
    versions_control: VersionsControl = field(default=None)
    participants: List[AccountWithPolicies] = field(default=None)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, source: dict) -> "BaseProject":
        return BaseProject(
            project_id=source.get("project_id"),
            title=source.get("title"),
            description=source.get("description"),
            last_updated=source.get("last_updated"),
            entity_created_date=source.get("entity_created_date"),
            resources={
                resource_id: Resource(**resource_data)
                for resource_id, resource_data in source.get("resources").items()
            },
            versions_control=VersionsControl(**source.get("versions_control")),
            participants=[
                AccountWithPolicies(
                    account_id=participant_policies.get("account_id"),
                    project=Policies.Project(**participant_policies.get("project")),
                    pages=Policies.Pages(**participant_policies.get("pages")),
                    items=Policies.Items(**participant_policies.get("items")),
                    media=Policies.Media(**participant_policies.get("media")),
                    users=Policies.Users(**participant_policies.get("users"))
                ) for participant_policies in source.get("participants")
            ],
        )

    def create_project(self):
        return repository.create_project(self.to_dict())

    def delete_project(self):
        repository.delete_project_by_id(self.project_id)

    @classmethod
    def get_project_by_id(cls, account_id: str) -> Optional["BaseProject"]:
        found_project = repository.get_project_by_id(account_id)
        if not found_project:
            return None
        return cls.from_dict(found_project)
