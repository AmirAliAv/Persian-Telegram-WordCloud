from telethon import TelegramClient
from telethon.tl.types import Dialog, MessageService, MessageMediaDocument, InputMessagesFilterVoice
import asyncio


class Crawler:
    def __init__(self, dialog: Dialog, client: TelegramClient, target_identifier, max_messages_count):
        super().__init__()
        self.dialog = dialog
        self.client = client
        self.targetId = self.get_user_entity(target_identifier).id
        self.max_messages_count = max_messages_count

    def get_user_entity(self, identifier):
        return asyncio.get_event_loop().run_until_complete(self.client.get_entity(identifier))

    def extract_messages_body(self):
        messages_text = []
        chat_name = self.dialog.name
        print('Chat Name: ', chat_name)

        i = 0
        for message in self.client.iter_messages(self.dialog, limit=None):
            if 0 <= self.max_messages_count <= i:  # if it's lower than zero, continue to the final message
                break
            i += 1
            if message.message is None or len(message.message) == 0:
                continue
            message_id = message.id
            body = message.message
            from_id = message.from_id
            if from_id == self.targetId:
                messages_text.append(body)
            fwd_from = message.fwd_from
            if fwd_from is not None:
                fwd_from = fwd_from.from_id
            reply_to_msg_id = message.reply_to_msg_id
            date = message.date

        return messages_text
