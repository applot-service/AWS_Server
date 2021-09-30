from collections import defaultdict
from ApplotLibs.DataStructures.MessageBus.Commands import Account as AccountCommands
from ApplotLibs.DataStructures.MessageBus.Commands import Projects as ProjectsCommands

from modules.CommandHandlers import Account as AccountCommandHandlers
from modules.CommandHandlers import Projects as ProjectsCommandHandlers


class CommandDeserializator:
    # Building command from source
    def __init__(self):
        self.command_classes = defaultdict(dict)
        self._set_up_account_commands()
        self._set_up_projects_commands()

    def _set_up_account_commands(self):
        self.command_classes["Account"]["SignIn"] = AccountCommands.SignIn
        self.command_classes["Account"]["SignOut"] = AccountCommands.SignOut
        self.command_classes["Account"]["Register"] = AccountCommands.Register

    def _set_up_projects_commands(self):
        self.command_classes["Projects"]["Pull"] = ProjectsCommands.Pull
        self.command_classes["Projects"]["CreateProject"] = ProjectsCommands.CreateProject

    def build_class(self, command_source: dict):
        command_type = command_source.get("command_type")
        command_action = command_source.get("command_action")
        command_class = self.command_classes[command_type][command_action]
        if not command_class:
            raise Exception
        return command_class.from_dict(command_source)


class Router:
    # Routing command source, executing command
    def __init__(self, command_source):
        self.command_source = command_source
        self.command_instance = None

        self.command_handlers = defaultdict(dict)
        self._set_up_account_handlers()
        self._set_up_projects_handlers()

    def _set_up_account_handlers(self):
        self.command_handlers["Account"]["SignIn"] = AccountCommandHandlers.auth_user
        self.command_handlers["Account"]["Register"] = AccountCommandHandlers.create_user

    def _set_up_projects_handlers(self):
        self.command_handlers["Projects"]["Pull"] = None  # "ProjectsCommandHandlers.Pull"
        self.command_handlers["Projects"]["CreateProject"] = None  # "ProjectsCommandHandlers.CreateProject"

    def create_command(self):
        self.command_instance = CommandDeserializator().build_class(command_source=self.command_source)
        return self

    def exec_command(self):
        command_type = self.command_instance.command_type
        command_action = self.command_instance.command_action
        command_handler = self.command_handlers[command_type][command_action]
        if not command_handler:
            raise Exception
        return command_handler(self.command_instance)
