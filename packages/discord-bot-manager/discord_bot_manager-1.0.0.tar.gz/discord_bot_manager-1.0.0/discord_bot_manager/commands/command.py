from discord_bot_manager.utils.formatter import get_help_text_from_list
from .types import MessageObj


class CommandManager:
    COMMANDS = []

    def __init__(self):
        self.activators: dict = {command.get_activator(): command for command in self.COMMANDS}

    async def parse_command(self, command: str, message_obj: MessageObj = None) -> str:
        main_command = command.split(" ", 1)[0].strip()

        if main_command in self.activators:
            command_executor = self.activators[main_command]
            return await command_executor.process_request(command, message_obj)
        elif main_command == "help":
            return self.create_help_text_from_list()

    def create_help_text_from_list(self) -> str:
        return get_help_text_from_list(self.COMMANDS)


class BaseCommand:
    SUB_COMMANDS: list = []
    ACTIVATOR: str = None

    def __init__(self):
        self.__activator = self.ACTIVATOR if self.ACTIVATOR is not None else str(self.__class__.__name__.lower())
        self.activators: dict = {command.get_activator(): command for command in self.SUB_COMMANDS}

    def get_activator(self) -> str:
        return self.__activator

    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        raise NotImplementedError

    def get_help_text(self) -> str:
        raise NotImplementedError

    def get_command_syntax(self) -> str:
        raise NotImplementedError

    async def parse_command(self, command: str, message_obj: MessageObj):
        main_command = command.split(" ", 1)[0].strip()

        if main_command in self.activators:
            command_executor = self.activators[main_command]
            if command.endswith(" help"):
                _help = command_executor.get_help_text()
                if help_for_sub_commands := command_executor.create_help_text_from_list(_help):
                    _help += "\n"
                    _help += "-" * int(len(_help) * 1.3)
                    _help += f"\n{help_for_sub_commands}"
                return _help

            return await command_executor.process_request(command, message_obj)
        elif main_command == "help":
            return self.create_help_text_from_list()

    def create_help_text_from_list(self, main_command_help_text=None) -> str:
        return get_help_text_from_list(self.SUB_COMMANDS, self.get_activator(), main_command_help_text)

    def __str__(self):
        return self.get_activator()


def auto_parse_sub_commands(func):
    async def wrapper(self, command, *args, **kwargs):
        new_command = command.replace(self.get_activator(), "").strip()
        sub_command_data = await self.parse_command(new_command, *args, **kwargs)

        if sub_command_data is not None:
            return sub_command_data
        else:
            return await func(self, command, *args, **kwargs)

    return wrapper


def handle_response_error(message="Something wrong happened !"):
    def inner(func):
        async def wrapper(self, command_text, *args, **kwargs):
            try:
                return await func(self, command_text, *args, **kwargs)
            except Exception as e:
                return str(e) if message is None else message

        return wrapper

    return inner


def get_args_only(func):
    async def wrapper(self, command_text, *args, **kwargs):
        return await func(self, command_text.replace(self.get_activator(), "").strip(), *args, **kwargs)

    return wrapper
