from .command import CommandManager
from .types import MessageObj
import discord


class DiscordClient(discord.Client):
    def __init__(self, command_mgr, **options):
        super().__init__(**options)
        self.command_mgr: CommandManager = command_mgr
        self.channels = {}

    def cache_channels_name(self):
        for channel in self.get_all_channels():
            if type(channel) == discord.channel.TextChannel:
                self.channels[channel.name] = channel

    async def on_ready(self):
        self.cache_channels_name()
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author != self.user:
            if resp := await self.command_mgr.parse_command(message.content, MessageObj(message=message, client=self)):
                await self.send_message(resp, message.channel)

    async def send_message(self, message, channel):
        if type(channel) == str:
            if channel := self.channels.get(channel):
                await channel.send(message)
            else:
                raise Exception(f"Text Channel {channel} doesn't exits.")
        else:
            await channel.send(message)
