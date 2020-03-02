from loader import ConfigLoader
from telegram_crawler.extractor import extract_dialogs
from persian_wordcloud.persian_wordcloud_drawer import draw_word_cloud


if __name__ == '__main__':
    config = ConfigLoader.get_config()
    messages = extract_dialogs(config)
    draw_word_cloud(messages, config['background_color'], config['color_map'])
