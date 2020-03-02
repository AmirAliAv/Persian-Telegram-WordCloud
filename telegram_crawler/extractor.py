from telegram_crawler.crawler import Crawler
from telegram_crawler.connector import Connector
import asyncio


async def get_dialogs(connector):
    return await connector.client.get_dialogs()


def extract_dialogs(config):
    c = Connector(config['api_id'], config['api_hash'], config['phone_number'])
    dialogs_name = config['dialogs_name']
    max_dialog_count = config['max_dialog_count']
    target_identifier = config['target_identifier']

    if target_identifier == 'me':
        target_identifier = config['phone_number']

    if config['crawl_all_of_dialog']:
        max_messages_count = -1
    else:
        if len(dialogs_name) == 0:
            max_messages_count = 1000
        else:
            max_messages_count = 10000

    dialogs = asyncio.get_event_loop().run_until_complete(get_dialogs(c))

    messages = []

    print('Number of your dialogs: ' + str(len(dialogs)))

    if len(dialogs_name) == 0:
        n = min(len(dialogs), max_dialog_count)

        for i in range(n):
            dialog = dialogs[i]
            print('dialog {} / {}'.format(i, n))
            crawler = Crawler(dialog, c.client, target_identifier, max_messages_count)
            messages.extend(crawler.extract_messages_body())

    else:
        n = len(dialogs)
        for i in range(n):
            dialog = dialogs[i]
            print('dialog {} / {}'.format(i, n))
            if dialog.name in dialogs_name:
                crawler = Crawler(dialog, c.client, target_identifier, max_messages_count)
                messages.extend(crawler.extract_messages_body())

    return messages
