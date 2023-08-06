from discord.message import Message


class MessageObj:
    def __init__(self, message, client):
        from .discord import DiscordClient

        self.message: Message = message
        self.client: DiscordClient = client
