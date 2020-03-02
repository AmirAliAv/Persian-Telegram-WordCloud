from crawler import Crawler
from loader import Connector
from database_manager import Database
from loader import ConfigLoader
import asyncio


async def get_dialogs(connector):
    return await connector.client.get_dialogs()


def extract_dialogs_from_telegram_server():
    db = Database(ConfigLoader.get_config())
    db.create_telegram_messages_table()
    c = Connector()

    dialogs = asyncio.get_event_loop().run_until_complete(get_dialogs(c))

    print('Dialogs: ' + str(len(dialogs)))

    n = len(dialogs)
    i = 0
    for dialog in dialogs:
        i += 1
        # if i > 2: exit()
        print('dialog {} / {}'.format(i, n))
        crawler = Crawler(dialog=dialog, client=c.client, database=Database(ConfigLoader.get_config()))
        crawler.go()


if __name__ == '__main__':
    extract_dialogs_from_telegram_server()
