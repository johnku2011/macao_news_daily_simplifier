# -*- coding: utf-8 -*-
import jieba
from textrank4zh import TextRank4Sentence
import pandas as pd

import time
import requests
from bs4 import BeautifulSoup

# function to extract title and content from news detail
def extract_title_and_contents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title_element = soup.find(
        "td", style="padding-left: 6px;padding-top:10px;padding-bottom:10px;")
    title = title_element.text.strip()

    content_elements = soup.find_all("founder-content")
    child_texts = [element.text.strip() for element in content_elements]

    return title, child_texts

def chinese_summarization(text, num_sentences=1):

    if isinstance(text, list):
        # Convert the list to a string
        text = " ".join(text)

    if isinstance(text, str):
        # Tokenize the Chinese text using jieba
        tokens = jieba.cut(text)

        # Join the tokens back into a string
        tokenized_text = " ".join(tokens)

        # Initialize TextRank4Sentence
        tr4s = TextRank4Sentence()

        # Add the tokenized text for analysis
        tr4s.analyze(text=tokenized_text, lower=True, source='no_stop_words')

        # Get the top N sentences as the summary
        summarized_sentences = tr4s.get_key_sentences(num=num_sentences)

        # Join the summarized sentences into a string
        summarized_text = " ".join([s.sentence for s in summarized_sentences])

        summarized_text_trim = summarized_text.replace(" ", "")

        return summarized_text_trim
    else:
        return ''

#--------------------------------------------------------------------------------------#
# Preprocessing function


def preprocess_text(text):
    # Chinese text segmentation
    segmented_text = jieba.cut(text)

    # Join the segmented words back into a single string
    preprocessed_text = ' '.join(segmented_text)

    return preprocessed_text

#--------------------------------------------------------------------------------------#