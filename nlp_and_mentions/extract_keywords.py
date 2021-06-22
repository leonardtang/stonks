import pandas as pd
import numpy as np

from collections import Counter
from PIL import Image
from expertai.nlapi.cloud.client import ExpertAiClient
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords
from string import punctuation

excluded_words = stopwords.words('english') + list(punctuation) + ['get', 'going', 'go']
client = ExpertAiClient()
language = 'en'


def extract_key_concepts():
    """
    Extracts the key words and phrases from today's WSB posts.
    Saves a DataFrame of two columns:
        1) The key word or phrase
        2) The number of times the word or phrase appeared in WSB today
    """

    df = pd.read_csv('data/wsb_daily_text.csv')
    text_column = df['text']

    all_concepts = []

    for i, text in text_column.iteritems():
        print(f'Extracting key concepts for post {i}')
        output = client.specific_resource_analysis(body={"document": {"text": text}},
                                                   params={'language': language, 'resource': 'relevants'})

        all_concepts.extend([lemma.value for lemma in output.main_lemmas])
        all_concepts.extend([phrase.value for phrase in output.main_phrases])

    ranked_concepts = Counter(all_concepts)
    concepts_df = pd.DataFrame.from_records([ranked_concepts]).transpose()
    concepts_df.to_csv('data/wsb_daily_concepts.csv')

    return ranked_concepts


def generate_wordcloud():
    """
    Generate and save a wordcloud based on the key concepts extracted via extract_key_concepts()
    }
    """

    key_concepts = extract_key_concepts()
    key_concepts = {concept: count for concept, count in key_concepts.items() if concept not in excluded_words}

    # Generate wordcloud color mask in the shape of the WSB logo
    wsb_color = np.array(Image.open('assets/wsb_full.jpeg'))
    wsb_mask = wsb_color.copy()
    wsb_mask[wsb_mask.sum(axis=2) == 0] = 255

    # edges = np.mean([gaussian_gradient_magnitude(wsb_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
    # wsb_mask[edges > .9] = 255

    # Generate wordcloud from top concepts
    wc = WordCloud(background_color='white', mask=wsb_mask, random_state=42)
    wc.fit_words(key_concepts)

    image_colors = ImageColorGenerator(wsb_color)
    wc.recolor(color_func=image_colors)

    img = wc.to_image()
    img.save('assets/daily_wordcloud.png')


if __name__ == "__main__":
    generate_wordcloud()

