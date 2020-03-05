from telegram_crawler.crawler import Crawler
from telegram_crawler.connector import Connector
from telethon.tl.types import Channel
import asyncio


def get_dialogs(client):
    return asyncio.get_event_loop().run_until_complete(client.get_dialogs())


def get_user_entity(client, identifier):
    return asyncio.get_event_loop().run_until_complete(client.get_entity(identifier))


def is_channel(dialog):
    return isinstance(dialog.entity, Channel) and not dialog.entity.megagroup


def extract_dialogs(config):
    c = Connector(config['api_id'], config['api_hash'], config['phone_number'])
    dialogs_name = config['dialogs_name']
    max_dialog_count = config['max_dialog_count']
    target_identifier = config['target_identifier']
    ignore_forwarded_messages = config['ignore_forwarded_messages']

    if target_identifier == 'me':
        target_identifier = config['phone_number']

    if len(target_identifier) == 0:
        target_entity_id = -1
    else:
        target_entity_id = get_user_entity(c.client, target_identifier).id

    if config['crawl_all_of_dialog']:
        max_messages_count = -1
    else:
        if len(dialogs_name) == 0:
            max_messages_count = 800
        else:
            max_messages_count = 4000

    dialogs = get_dialogs(c.client)

    messages = []

    print('Number of your dialogs: ' + str(len(dialogs)))

    if len(dialogs_name) == 0:
        n = min(len(dialogs), max_dialog_count, 1)

        i = 0
        for dialog in dialogs:
            if not is_channel(dialog):
                print('dialog {} / {}'.format(i, n))
                crawler = Crawler(dialog, c.client, target_entity_id, max_messages_count, ignore_forwarded_messages)
                messages.extend(crawler.extract_messages_body())
                i += 1
                if i >= n:
                    break

    else:
        n = len(dialogs)
        is_found = False
        for i in range(n):
            dialog = dialogs[i]
            print('dialog {} / {}'.format(i, n))
            if dialog.name in dialogs_name:
                is_found = True
                crawler = Crawler(dialog, c.client, target_entity_id, max_messages_count, ignore_forwarded_messages)
                messages.extend(crawler.extract_messages_body())

        if not is_found:
            raise Exception('None of candidate dialogs were found')

    return messages
