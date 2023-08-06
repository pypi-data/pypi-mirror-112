import spacy
if not spacy.util.is_package("en_core_web_sm"):
    python spacy -m download ru_core_news_sm