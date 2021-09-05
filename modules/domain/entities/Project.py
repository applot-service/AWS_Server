from dataclasses import dataclass, field, asdict

from modules.domain import repository
from ApplotLibs.DataStructures import Project, Policies

from typing import Optional


@dataclass
class Resource(Project.Resource):
    pass


@dataclass
class VersionsControl(Project.VersionsControl):
    pass


@dataclass
class AccountWithPolicies(Project.AccountWithPolicies):
    pass


@dataclass
class BaseProject(Project.BaseProject):
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
            } if source.get("resources") else None,
            versions_control=VersionsControl(**source.get("versions_control")) if
            source.get("versions_control") else VersionsControl(),
            participants={
                account_id: AccountWithPolicies(
                    account_id=account_policies.get("account_id"),
                    project=Policies.Project(**account_policies.get("project")),
                    pages=Policies.Pages(**account_policies.get("pages")),
                    items=Policies.Items(**account_policies.get("items")),
                    media=Policies.Media(**account_policies.get("media")),
                    users=Policies.Users(**account_policies.get("users"))
                ) for account_id, account_policies in source.get("participants")
            } if source.get("participants") else None
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
