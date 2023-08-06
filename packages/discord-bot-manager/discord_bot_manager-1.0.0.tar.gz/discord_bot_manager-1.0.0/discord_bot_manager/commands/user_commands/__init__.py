from discord_bot_manager.commands.command import BaseCommand, auto_parse_sub_commands

from .utils import CurrentTime, RandomNumber, Calc, SetTimer, SendMessage
from .ai import Search, Chat
from ..types import MessageObj


class Main(BaseCommand):
    ACTIVATOR = "bot"
    SUB_COMMANDS = [
        CurrentTime(), RandomNumber(), Calc(), SetTimer(), SendMessage(),
        Search(), Chat()
    ]

    @auto_parse_sub_commands
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        return "Hey, How are you doing !! You can type `main help` to get list of available commands."

    def get_help_text(self):
        return "Entry point for other commands."

    def get_command_syntax(self) -> str:
        return self.get_activator()
