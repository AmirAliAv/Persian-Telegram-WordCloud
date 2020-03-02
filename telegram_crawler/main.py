from crawler import Crawler
from connector import Connector
from loader import ConfigLoader
import asyncio


async def get_dialogs(connector):
    return await connector.client.get_dialogs()


def extract_dialogs_from_telegram_server():
    config = ConfigLoader.get_config()

    c = Connector(config['api_id'], config['api_hash'], config['phone_number'])
    candidate_dialog_names = config['candidate_dialog_names']
    max_dialog_count = config['max_dialog_count']
    target_identifier = config['target_identifier']

    dialogs = asyncio.get_event_loop().run_until_complete(get_dialogs(c))

    messages = []

    print('Number of your dialogs: ' + str(len(dialogs)))

    if len(candidate_dialog_names) == 0:
        n = min(len(dialogs), max_dialog_count)

        for i in range(n):
            dialog = dialogs[i]
            print('dialog {} / {}'.format(i, n))
            crawler = Crawler(dialog=dialog, client=c.client, target_identifier=target_identifier)
            messages.extend(crawler.extract_messages_body())

    else:
        n = len(dialogs)
        for i in range(n):
            dialog = dialogs[i]
            print('dialog {} / {}'.format(i, n))
            if dialog.name in candidate_dialog_names:
                crawler = Crawler(dialog=dialog, client=c.client, target_identifier=target_identifier)
                messages.extend(crawler.extract_messages_body())

    return messages


if __name__ == '__main__':
    print(extract_dialogs_from_telegram_server())
