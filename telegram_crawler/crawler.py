from telethon import TelegramClient
from telethon.tl.functions.messages import GetDocumentByHashRequest
from telethon.tl.types import Dialog, MessageService, MessageMediaDocument, InputMessagesFilterVoice
from typing import List

from telethon.tl.types import DocumentAttributeAudio
from telethon.tl.types import Message

from database_manager import Database
import sys, traceback


class Crawler:
    def __init__(self, dialog: Dialog, client: TelegramClient, database: Database):
        super().__init__()
        self.dialog = dialog
        self.client = client
        self.database = database
        self.log = open("log.txt", "w")

    def go(self):
        for message in self.client.iter_messages(self.dialog, limit=None):
            if message.message is None or len(message.message) == 0:
                continue
            message_id = message.id
            body = message.message
            print(body)
            from_id = message.from_id
            fwd_from = message.fwd_from
            if fwd_from is not None:
                fwd_from = fwd_from.from_id
            reply_to_msg_id = message.reply_to_msg_id
            date = message.date
            chat_name = self.dialog.name

            try:
                self.database.insert_message(message_id, body, from_id, fwd_from, reply_to_msg_id, date, chat_name)
            except:
                print(message)
                traceback.print_exc(file=sys.stdout)
