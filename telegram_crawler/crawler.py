from telethon import TelegramClient
from telethon.tl.functions.messages import GetDocumentByHashRequest
from telethon.tl.types import Dialog, MessageService, MessageMediaDocument, InputMessagesFilterVoice
from typing import List

from telethon.tl.types import DocumentAttributeAudio
from telethon.tl.types import Message

import sys, traceback
import asyncio

# params
MAX_MSG_COUNT = 100


class Crawler:
    def __init__(self, dialog: Dialog, client: TelegramClient, target_identifier):
        super().__init__()
        self.dialog = dialog
        self.client = client
        self.targetId = self.get_user_entity(target_identifier).id

    def get_user_entity(self, identifier):
        return asyncio.get_event_loop().run_until_complete(self.client.get_entity(identifier))

    def extract_messages_body(self):
        messages_text = []
        chat_name = self.dialog.name
        print('Chat Name: ', chat_name)

        i = 0
        for message in self.client.iter_messages(self.dialog, limit=None):
            if i >= MAX_MSG_COUNT:
                break
            if message.message is None or len(message.message) == 0:
                continue
            message_id = message.id
            body = message.message
            from_id = message.from_id
            if from_id == self.targetId:
                i += 1
                messages_text.append(body)
            fwd_from = message.fwd_from
            if fwd_from is not None:
                fwd_from = fwd_from.from_id
            reply_to_msg_id = message.reply_to_msg_id
            date = message.date

        return messages_text
