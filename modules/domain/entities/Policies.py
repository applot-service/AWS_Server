from dataclasses import dataclass
from ApplotLibs.DataStructures import Policies


@dataclass
class Project(Policies.Project):
    pass


@dataclass
class Pages(Policies.Pages):
    pass


@dataclass
class Items(Policies.Items):
    pass


@dataclass
class Media(Policies.Media):
    pass


@dataclass
class Users(Policies.Users):
    pass
