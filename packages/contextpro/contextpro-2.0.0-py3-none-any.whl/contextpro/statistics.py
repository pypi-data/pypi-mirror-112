"""This module contains functions for calculating some text data
related statistics."""

import string
from typing import Any, Dict, Iterable, List, Optional, cast

import pandas as pd
from nltk.probability import FreqDist
from textblob import TextBlob

from contextpro._processing import (
    _is_nested_string_list,
    _is_string_list,
    _parallelize_func,
)
from contextpro.feature_extraction import batch_get_ngrams, get_ngrams
from contextpro.normalization import batch_lowercase_text, batch_remove_stopwords
from contextpro.tokenization import batch_tokenize_text


def get_ngram_counts(tokens: List[str], ngram_size: int = 1) -> Dict[str, int]:
    """Calculate ngram counts in a tokenized document.

    Parameters
    ----------
    tokens : List[str]
        list of tokens

    ngram_size : str, optional
        size of ngrams to calculate, by default 1 - unigrams

    Returns
    -------
    Dict[str, int]
        mapping from ngram to the number of occurrences in a document

    Raises
    ------
    ValueError
        if 'tokens' provided is not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import get_ngram_counts
    >>> tokens = ["my", "name", "is", "dr", "jekyll"]
    >>> get_ngram_counts(tokens, ngram_size=1)
    {'my': 1, 'name': 1, 'is': 1, 'dr': 1, 'jekyll': 1}
     >>> get_ngram_counts(tokens, ngram_size=2)
    {'my name': 1, 'name is': 1, 'is dr': 1, 'dr jekyll': 1}
    """

    if not _is_string_list(tokens):
        raise ValueError("'tokens' should be a list of strings")

    return _count_grams(get_ngrams(tokens, ngram_size=ngram_size))


def calculate_sentiment_score(document: str) -> float:
    """Calculate sentiment score for the sentence using TextBlob object.

    Parameters
    ----------
    document : str
        sentence which sentiment score has to be calculated

    Returns
    -------
    float
        float within [-1.0, 1.0] range representing sentiment score
        for the sentence, where -1.0 means negative and 1.0 positive

    Examples
    --------
    >>> from contextpro.statistics import calculate_sentiment_score
    >>> corpus = "I love the Spiderman movie"
    >>> calculate_sentiment_score(sentence)
    0.5
    """
    return float(TextBlob(document).polarity)


def calculate_subjectivity_score(document: str) -> float:
    """Calculate subjectivity score for the sentence using TextBlob object.

    Parameters
    ----------
    document : str
        sentence which subjectivity score has to be calculated

    Returns
    -------
    float
        float within [0.0, 1.0] range representing subjectivity score
        for the sentence, where 0.0 means very objective and 1.0 very
        subjective

    Examples
    --------
    >>> from contextpro.statistics import calculate_subjectivity_score
    >>> corpus = "I love the Spiderman movie"
    >>> calculate_subjectivity_score(sentence)
    0.6
    """
    return float(TextBlob(document).subjectivity)


def batch_get_ngram_counts(
    tokens: List[List[str]], ngram_size: int = 1
) -> Dict[str, int]:
    """Calculate ngram counts across the corpus of tokenized documents.

    Parameters
    ----------
    tokens : List[List[str]]
        list of nested token lists

    ngram_size : str, optional
        size of ngrams to calculate, by default 1 - unigrams

    Returns
    -------
    Dict[str, int]
        mapping from ngram to the number of occurrences in a
        corpus of tokenized documents

    Raises
    ------
    ValueError
        if 'tokens' provided is not a list of nested token lists

    Examples
    --------
    >>> from contextpro.statistics import get_ngram_counts
    >>> corpus = [
        ["my", "name", "is", "dr", "jekyll"],
        ["his", "name", "is", "mr", "hyde"],
        ["this", "guy", "name", "is", "edward", "scissorhands"],
        ["and", "this", "is", "tom", "parker"],
    ]
    >>> batch_get_ngram_counts(corpus, ngram_size=1)
    {
        'my': 1, 'name': 3, 'is': 4, 'dr': 1, 'jekyll': 1, 'his': 1,
        'mr': 1, 'hyde': 1, 'this': 2, 'guy': 1, 'edward': 1,
        'scissorhands': 1, 'and': 1, 'tom': 1, 'parker': 1
    }
    >>> batch_get_ngram_counts(corpus, ngram_size=2)
    {
        "my name": 1, "name is": 3, "is dr": 1, "dr jekyll": 1,
        "his name": 1, "is mr": 1, "mr hyde": 1, "this guy": 1,
        "guy name": 1, "is edward": 1, "edward scissorhands": 1,
        "and this": 1, "this is": 1, "is tom": 1, "tom parker": 1
    }
    """
    if not _is_nested_string_list(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return _batch_count_grams(batch_get_ngrams(tokens, ngram_size=ngram_size))


def batch_calculate_sentiment_scores(
    documents: List[str], num_workers: Optional[int] = None
) -> List[float]:
    """Calculate sentiment scores for sentences in a concurrent manner.

    Parameters
    ----------
    documents : List[str]
        list of sentences which sentiment scores have to be calculated

    num_workers : Optional[int]
        number of processors to use, by default None (all processors)

    Returns
    -------
    List[float]
        list of floats within [-1.0, 1.0] range representing sentiment scores
        for the sentences where -1.0 means negative and 1.0 positive

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_sentiment_scores
    >>> corpus = [
    ...     "I don't like you.",
    ...     "I love the Spiderman movie",
    ...     "In my opinion this movie was rather boring than exciting",
    ...     "This is the worst movie I've ever seen"
    ... ]
    >>> batch_calculate_sentiment_scores(
    ...     corpus,
    ...     num_workers=2
    ... )
    [0.0, 0.5, -0.35, -1.0]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[float],
        _parallelize_func(
            calculate_sentiment_score, documents, num_workers=num_workers
        ),
    )


def batch_calculate_subjectivity_scores(
    documents: List[str], num_workers: Optional[int] = None
) -> List[float]:
    """Calculate subjectivity scores for sentences in a concurrent manner.

    Parameters
    ----------
    documents : List[str]
        list of sentences which subjectivity scores have to be calculated

    num_workers : Optional[int]
        number of processors to use, by default None (all processors)

    Returns
    -------
    List[float]
        list of floats within [0.0, 1.0] range representing subjectivity scores
        for the sentences where 0.0 means very objective and 1.0 very
        subjective

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_subjectivity_scores
    >>> corpus = [
    ...     "I don't like you.",
    ...     "I love the Spiderman movie",
    ...     "In my opinion this movie was rather boring than exciting",
    ...     "This is the worst movie I've ever seen"
    ... ]
    >>> batch_calculate_subjectivity_scores(
    ...     corpus,
    ...     num_workers=2
    ... )
    [0.0, 0.6, 0.9, 1.0]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[float],
        _parallelize_func(
            calculate_subjectivity_score, documents, num_workers=num_workers
        ),
    )


def batch_calculate_corpus_statistics(
    documents: List[str],
    lowercase: bool = False,
    remove_stopwords: bool = False,
    tokenizer_pattern: str = r"\b[^\d\W]+\b",
    custom_stopwords: List[str] = [],
    num_workers: Optional[int] = None,
) -> pd.DataFrame:
    r"""Calculates the below statistics for each document in the corpus
    in a concurrent manner:

        - Number of characters
        - Number of tokens
        - Number of punctuation characters
        - Number of digits
        - Number of whitespace characters
        - Number of non-ascii characters
        - Sentiment score
        - Subjectivity score

    Parameters
    ----------
    documents : List[str]
        list of strings

    lowercase : bool, optional
        convert all characters to lowercase before calculating
        statistics, by default False

    remove_stopwords : bool, optional
        remove stopwords before calculating statistics. Uses english
        stopwords from the NLTK library if 'custom_stopwords'
        list is not provided, by default False

    tokenizer_pattern : str, optional
        regex pattern used by the underlying NLTK Regexp Tokenizer
        to tokenize the documents, by default r"\b[^\d\W]+\b"

    custom_stopwords : List[str], optional
        custom stopwords to use for token filtering, by default []

    num_workers : Optional[int], optional
        number of processors to use, by default None (all processors)

    Returns
    -------
    pd.DataFrame
        with statistics for each document in the provided corpus

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_corpus_statistics
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> batch_calculate_corpus_statistics(
    ...     corpus,
    ...     lowercase=False,
    ...     remove_stopwords=False,
    ...     num_workers=2,
    ... )
        characters  tokens  punctuation_characters  digits  whitespace_characters  \
    0          22       5                       2       0                      4
    1          20       5                       1       0                      4
    2          38       7                       1       0                      5
    3          22       5                       0       0                      4

    ascii_characters  sentiment_score  subjectivity_score
    0                22              0.0                 0.0
    1                20              0.0                 0.0
    2                38              0.0                 0.0
    3                22              0.0                 0.0
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    if lowercase:
        documents = batch_lowercase_text(documents)

    tokens = batch_tokenize_text(
        documents,
        tokenizer_method="nltk_regexp_tokenizer",
        pattern=tokenizer_pattern,
        gaps=False,
        num_workers=num_workers,
    )

    if remove_stopwords:
        tokens = batch_remove_stopwords(
            tokens, custom_stopwords=custom_stopwords, num_workers=num_workers
        )

    num_chars = _batch_calculate_lengths(documents, num_workers=num_workers)
    num_tokens = _batch_calculate_lengths(tokens, num_workers=num_workers)
    sentiment_scores = batch_calculate_sentiment_scores(
        documents, num_workers=num_workers
    )
    subjectivity_scores = batch_calculate_subjectivity_scores(
        documents, num_workers=num_workers
    )
    num_punct = _batch_calculate_chars(
        documents, character_type="punctuation", num_workers=num_workers
    )
    num_digits = _batch_calculate_chars(
        documents, character_type="digits", num_workers=num_workers
    )
    num_whitespace = _batch_calculate_chars(
        documents, character_type="whitespace", num_workers=num_workers
    )
    num_ascii = _batch_calculate_chars(
        documents, character_type="ascii", num_workers=num_workers
    )

    statistics = pd.DataFrame(
        {
            "characters": num_chars,
            "tokens": num_tokens,
            "punctuation_characters": num_punct,
            "digits": num_digits,
            "whitespace_characters": num_whitespace,
            "ascii_characters": num_ascii,
            "sentiment_score": sentiment_scores,
            "subjectivity_score": subjectivity_scores,
        }
    )

    return statistics


def _calculate_chars(document: str, character_type: str = "ascii") -> int:
    """Calculate the number of characters of a chosen type in the document."""
    if character_type == "punctuation":
        chars_to_filter = set(string.punctuation)
    elif character_type == "digits":
        chars_to_filter = set(string.digits)
    elif character_type == "ascii":
        chars_to_filter = set(string.printable)
    elif character_type == "whitespace":
        chars_to_filter = set(string.whitespace)
    count = len(list(filter(lambda char: char in chars_to_filter, document)))
    return count


def _batch_calculate_lengths(
    iterable: Iterable[Any], num_workers: Optional[int] = None
) -> Iterable[int]:
    """Calculate lengths of items in the iterable in a concurrent manner."""
    return _parallelize_func(len, iterable, num_workers=num_workers)


def _batch_calculate_chars(
    documents: List[str],
    character_type: str = "ascii",
    num_workers: Optional[int] = None,
) -> Iterable[int]:
    """Count the number of characters of a chosen type across the
    document corpus in a concurrent manner.
    """
    return _parallelize_func(
        _calculate_chars,
        documents,
        character_type=character_type,
        num_workers=num_workers,
    )


def _count_grams(ngrams: List[str]) -> Dict[str, int]:
    """Calculate n-gram counts in a document."""
    dist = FreqDist(ngrams)
    return {ngram: count for ngram, count in zip(dist.keys(), dist.values())}


def _batch_count_grams(ngrams: List[List[str]]) -> Dict[str, int]:
    """Calculate n-gram counts for the corpus of documents"""
    flat_grams = [ngram for doc in ngrams for ngram in doc]
    return _count_grams(flat_grams)


__all__ = [
    "get_ngram_counts",
    "batch_get_ngram_counts",
    "calculate_sentiment_score",
    "calculate_subjectivity_score",
    "batch_calculate_sentiment_scores",
    "batch_calculate_subjectivity_scores",
    "batch_calculate_corpus_statistics",
]
