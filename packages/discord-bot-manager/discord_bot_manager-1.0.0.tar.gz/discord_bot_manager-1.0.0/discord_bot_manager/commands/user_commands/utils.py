import asyncio
import datetime
import random

from discord_bot_manager.commands.command import (
    BaseCommand,
    handle_response_error,
    get_args_only
)
from ..types import MessageObj


class CurrentTime(BaseCommand):
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        return f"{datetime.datetime.now():'%Y-%d-%m, %H:%M:%S'}"

    def get_help_text(self):
        return "Get current Date and Time."

    def get_command_syntax(self) -> str:
        return self.get_activator()


class RandomNumber(BaseCommand):
    @handle_response_error(message="Invalid, type help for getting syntax")
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        numbers = command_text.split(" ")
        return str(random.randint(int(numbers[-2]), int(numbers[-1])))

    def get_help_text(self):
        return f"Get Random number between given range."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <NUM1> <NUM2>"


class Calc(BaseCommand):
    @handle_response_error(message="Invalid Expression, Must be valid mathematical Expression.")
    @get_args_only
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        if "**" in command_text:
            _, power = command_text.split("**", 1)
            if len(power) > 2:
                return "can't have more than two digits after **."

        allowed_chars = "1234567890!@#$%^&*()_+=-|][{}\\;/."
        for c in command_text:
            if c not in allowed_chars:
                return "Please give a valid mathematical expression."

        return str(eval(command_text))

    def get_help_text(self):
        return "Calculate mathematical expressions."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <MATHEMATICAL EXPRESSION>"


class SetTimer(BaseCommand):
    @handle_response_error(message="Invalid !!")
    @get_args_only
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        args = command_text.split(" ", 1)
        time, msg = args[0].strip(), " ".join(args[1:])
        await asyncio.sleep(int(time))
        return msg or f"Timer for {time} seconds over !!"

    def get_help_text(self):
        return "sets timer for given seconds."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <TIME IN SECONDS> <MESSAGE TO DISPLAY WHEN OVER>[OPT]"


class SendMessage(BaseCommand):
    @handle_response_error(message=None)
    @get_args_only
    async def process_request(self, command_text: str, message_obj: MessageObj) -> str:
        channel, message = command_text.split(" ", 1)
        await message_obj.client.send_message(
            f"`{message_obj.message.author}` from channel `{message_obj.message.channel.name}` said `{message}`",
            channel
        )
        return ""

    def get_help_text(self):
        return "Sends message to the specified channel."

    def get_command_syntax(self) -> str:
        return f"{self.get_activator()} <CHANNEL NAME> <MESSAGE TO SEND>"
