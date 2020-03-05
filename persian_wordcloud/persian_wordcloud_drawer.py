import re
import codecs
import numpy as np
from PIL import Image
from hazm import *
import arabic_reshaper
from bidi.algorithm import get_display
from wordcloud_fa import WordCloudFa


# Params
FONT_PATH = "fonts/XTitre.TTF"
# FONT_PATH = "fonts/Aerolite Bold.otf"  # suitable for english characters

MASK_PATH = "mask.png"

STOPWORDS_PATH = "stopwords.dat"
SAVE_PATH = "word_cloud.png"


def draw_word_cloud(sentences, background_color='black', color_map='Blues_r', ignore_english_characters=True,
                    mask_path=MASK_PATH, font_path=FONT_PATH):
    # Normalize words
    tokenizer = WordTokenizer()
    lemmatizer = Lemmatizer()
    normalizer = Normalizer()
    stopwords = set(list(map(lambda w: w.strip(), codecs.open(STOPWORDS_PATH, encoding='utf8'))))
    words = []
    for sentence in sentences:
        sentence = re.sub(r"[,.;:?!،()؟]+", " ", sentence)
        if ignore_english_characters:
            sentence = re.sub('[^\u0600-\u06FF]+', " ", sentence)  # remove english characters
        sentence = re.sub(r'[\u200c\s]*\s[\s\u200c]*', " ", sentence)
        sentence = re.sub(r'[\u200c]+', " ", sentence)
        sentence = re.sub(r'[\n]+', " ", sentence)
        sentence = re.sub(r'[\t]+', " ", sentence)
        sentence = normalizer.normalize(sentence)
        sentence = normalizer.character_refinement(sentence)
        sentence_words = tokenizer.tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(w).split('#', 1)[0] for w in sentence_words]  # finding the root of each word
        sentence_words = list(filter(lambda x: x not in stopwords, sentence_words))
        words.extend(sentence_words)
    print(words)

    # Build word_cloud
    mask = np.array(Image.open(mask_path))
    clean_string = ' '.join([str(elem) for elem in words])
    clean_string = arabic_reshaper.reshape(clean_string)
    clean_string = get_display(clean_string)
    word_cloud = WordCloudFa(persian_normalize=False, mask=mask, colormap=color_map,
                             background_color=background_color, include_numbers=False, font_path=font_path)
    wc = word_cloud.generate(clean_string)
    image = wc.to_image()
    image.show()
    image.save(SAVE_PATH)

    print('\nThe WordCloud image is saved in ' + SAVE_PATH)
