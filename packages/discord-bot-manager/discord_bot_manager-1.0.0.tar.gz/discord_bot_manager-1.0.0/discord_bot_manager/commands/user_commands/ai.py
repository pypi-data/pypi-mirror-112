import re

from discord_bot_manager.commands.command import (
    BaseCommand,
    auto_parse_sub_commands,
    get_args_only
)
from discord_bot_manager.utils.search import search
from ..types import MessageObj


class Search(BaseCommand):
    @get_args_only
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        return search(command_text)

    def get_help_text(self):
        return "Searches the internet for your query."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <QUERY>"


class Chat(BaseCommand):
    ACTIVATOR = "ai"

    @auto_parse_sub_commands
    @get_args_only
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        known_queries = re.compile("(who is|what is|how to)")

        if known_queries.match(command_text):
            return search(command_text)
        else:
            return "WHAT ??"

    def get_help_text(self):
        return "Tries to give response to your queries."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <QUERY>"
