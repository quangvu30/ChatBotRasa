from rasa.core.channels.facebook import MessengerBot
from rasa.core.channels.facebook import MessengerClient

class Facebook:

    client: MessengerClient
    bot: MessengerBot

    def __init__(self, page_access_token: str):
        self.client = MessengerClient(page_access_token)
        self.bot = MessengerBot(self.client)

    async def send_text(self,recipient_id: str, text : str):
        await self.bot.send_text_message(recipient_id, text)