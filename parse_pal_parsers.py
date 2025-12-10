"""
Nancy Guan
DS3500
Homework 7: Natural Language Processing
5 December 2025
parse_pal_parsers.py
"""
import re
from collections import Counter

@staticmethod
def default_parser(filename):
    """ Parses generic plain text files and provides statistics"""
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    raw_text = text
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()

    words = text_clean.split()
    wordcount = Counter(words)
    numwords = len(words)

    avg_word_length = sum(len(word) for word in words) / numwords if numwords > 0 else 0

    sentences = re.split(r'[.!?]+', raw_text)
    num_sentences = len([s for s in sentences if s.strip()])
    avg_sentence_length = numwords / num_sentences if num_sentences > 0 else 0

    unique_words = len(set(words))
    lexical_diversity = unique_words / numwords if numwords > 0 else 0

    results = {
        'wordcount': wordcount,
        'word_count': wordcount,
        'numwords': numwords,
        'raw_text': raw_text,
        'clean_text': text_clean,
        'avg_word_length': avg_word_length,
        'num_sentences': num_sentences,
        'avg_sentence_length': avg_sentence_length,
        'unique_words': unique_words,
        'lexical_diversity': lexical_diversity
    }
    print(f"{filename}: {numwords} words")
    return results

@staticmethod
def propaganda_parser(filename):
    """ Domain-specific parser for propaganda files"""
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    raw_text = text
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()

    words = text_clean.split()
    wordcount = Counter(words)
    numwords = len(words)
    avg_word_length = sum(len(word) for word in words) / numwords if numwords > 0 else 0

    sentences = re.split(r'[.!?]+', raw_text)
    num_sentences = len([s for s in sentences if s.strip()])
    avg_sentence_length = numwords / num_sentences if num_sentences > 0 else 0

    unique_words = len(set(words))
    lexical_diversity = unique_words / numwords if numwords > 0 else 0
    exclamation_count = raw_text.count('!')
    question_count = raw_text.count('?')

    bigrams = [' '.join(words[i:i + 2]) for i in range(len(words) - 1)]
    trigrams = [' '.join(words[i:i + 3]) for i in range(len(words) - 2)]
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)

    most_repeated_bigram = bigram_counts.most_common(1)[0] if bigram_counts else ('', 0)
    most_repeated_trigram = trigram_counts.most_common(1)[0] if trigram_counts else ('', 0)

    results = {
        'wordcount': wordcount,
        'word_count': wordcount,
        'numwords': numwords,
        'raw_text': raw_text,
        'clean_text': text_clean,
        'avg_word_length': avg_word_length,
        'num_sentences': num_sentences,
        'avg_sentence_length': avg_sentence_length,
        'unique_words': unique_words,
        'lexical_diversity': lexical_diversity,
        'exclamation_count': exclamation_count,
        'question_count': question_count,
        'most_repeated_bigram': most_repeated_bigram,
        'most_repeated_trigram': most_repeated_trigram
    }
    print(f"{filename}: {numwords} words")
    return results