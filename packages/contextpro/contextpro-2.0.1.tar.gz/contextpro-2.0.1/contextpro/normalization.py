"""This module contains functions for text data normalization."""

import re
import string
from typing import Any, List, Optional, cast

import contractions
import spacy
from nltk.corpus import stopwords
from nltk.stem import (
    LancasterStemmer,
    PorterStemmer,
    RegexpStemmer,
    SnowballStemmer,
    WordNetLemmatizer,
)
from word2number import w2n

from contextpro._processing import (
    _is_nested_string_list,
    _is_string_list,
    _parallelize_func,
)

nlp = spacy.load("en_core_web_sm")


def remove_stopwords(tokens: List[str], custom_stopwords: List[str] = []) -> List[str]:
    """Remove stopwords from the provided list of tokens.

    Parameters
    ----------
    tokens : List[str]
        list of tokens, including stopwords
    custom_stopwords : List[str], optional
        which should be removed from the list of tokens, by default []

    Returns
    -------
    List[str]
        list of tokens without stopwords

    Examples
    --------
    >>> from contextpro.normalization import remove_stopwords
    >>> tokens = ['My', 'name', 'is', 'Dr', 'Jekyll']
    >>> remove_stopwords(tokens)
    ['My', 'name', 'Dr', 'Jekyll']
    """
    if custom_stopwords:
        stop_words = set(custom_stopwords)
    else:
        stop_words = set(stopwords.words("english"))
    return [word for word in tokens if word not in stop_words]


def remove_non_ascii_characters(sentence: str) -> str:
    """Removes non-ascii characters from the provided sentence.

    Parameters
    ----------
    sentence : str
        with non-ascii characters

    Returns
    -------
    str
        without non-ascii characters

    Examples
    --------
    >>> from contextpro.normalization import remove_non_ascii_characters
    >>> sentence = "https://sitebulb.com/Folder/øê.html?大学"
    >>> remove_non_ascii_characters(sentence)
    'https://sitebulb.com/Folder/.html?'
    """
    printable_chars = set(string.printable)
    return "".join(filter(lambda char: char in printable_chars, sentence))


def remove_punctuation(sentence: str) -> str:
    """Removes punctuation characters from the sentence.

    Parameters
    ----------
    sentence : str
        with punctuation characters

    Returns
    -------
    str
        without punctuation characters

    Examples
    --------
    >>> from contextpro.normalization import remove_punctuation
    >>> corpus = "My name is Dr. Jekyll."
    >>> remove_punctuation(sentence)
    'My name is Dr Jekyll'
    """
    punctuation_chars = set(string.punctuation)
    return "".join(filter(lambda char: char not in punctuation_chars, sentence))


def remove_numbers(sentence: str) -> str:
    """Removes numbers from the sentence.

    Parameters
    ----------
    sentence : str
        with number characters

    Returns
    -------
    str
        without number characters

    Examples
    --------
    >>> from contextpro.normalization import remove_numbers
    >>> sentence = "He is 12 years old."
    >>> remove_numbers(sentence)
    'He is  years old.'
    """
    digit_chars = set(string.digits)
    return "".join(filter(lambda char: char not in digit_chars, sentence))


def remove_whitespace(sentence: str) -> str:
    """Removes whitespace characters from the sentence.

    Parameters
    ----------
    sentence : str
        with whitespace characters

    Returns
    -------
    str
        without whitespace characters

    Examples
    --------
    >>> from contextpro.normalization import remove_whitespace
    >>> sentence = "He Has Not Been    in Touch for over a Month."
    >>> remove_whitespace(sentence)
    'He Has Not Been in Touch for over a Month.'
    """
    return " ".join(re.split(r"\s+", sentence, flags=re.UNICODE))


def convert_numerals_to_numbers(sentence: str) -> str:
    """Replaces numerals with numbers in a sentence.

    Parameters
    ----------
    sentence : str
        with numerals

    Returns
    -------
    str
        with numerals replaced with numbers

    Examples
    --------
    >>> from contextpro.normalization import convert_numerals_to_numbers
    >>> sentence = "A bunch of five"
    >>> convert_numerals_to_numbers(sentence)
    'A bunch of 5'
    """
    spacy_doc = nlp(sentence)
    try:
        tokens = [
            w2n.word_to_num(token.text) if token.pos_ == "NUM" else token.text
            for token in spacy_doc
        ]
    except ValueError:
        return sentence
    return " ".join([str(token) for token in tokens])


def replace_contractions(sentence: str, **kwargs: bool) -> str:
    """Expands contractions in a sentence.

    Parameters
    ----------
    sentence : str
        with contracted words

    Other Parameters
    ----------------
    **kwargs : bool
        additional properties of the below method:
            - contractions.fix()

    Returns
    -------
    str
        without contracted words

    Examples
    --------
    >>> from contextpro.normalization import replace_contractions
    >>> sentence = "I don't want to be rude, but you shouldn't do this"
    >>> replace_contractions(sentence)
    'I do not want to be rude, but you should not do this'
    """
    return cast(str, contractions.fix(sentence, **kwargs))


def stem(
    tokens: List[str],
    stemmer_type: Optional[str] = "nltk_porter_stemmer",
    **kwargs: Any,
) -> List[str]:
    """Reduces tokens to their root (base) form.

    Parameters
    ----------
    tokens : List[str]
        list of tokens containing words with various inflectional forms

    stemmer_type : Optional[str], optional
        stemmer type which will be used to stem the tokens,
        by default "nltk_porter_stemmer"

        Allowed values:
          - nltk_porter_stemmer
          - nltk_lancaster_stemmer
          - nltk_regexp_stemmer
          - nltk_snowball_stemmer

    Other Parameters
    ----------------
    **kwargs : Any
        additional properties of the below stemmers:
          - nltk.PorterStemmer
          - nltk.LancasterStemmer
          - nltk.RegexpStemmer
          - nltk.SnowballStemmer

    Returns
    -------
    List[str]
        list of stemmed tokens

    Examples
    --------
    >>> from contextpro.normalization import stem
    >>> tokens =  ["I", "like", "driving", "a", "car"]
    >>> stem(tokens, stemmer_type="nltk_porter_stemmer")
    ['I', 'like', 'drive', 'a', 'car']
    """
    if stemmer_type == "nltk_porter_stemmer":
        stemmer = PorterStemmer(**kwargs)
    elif stemmer_type == "nltk_lancaster_stemmer":
        stemmer = LancasterStemmer(**kwargs)
    elif stemmer_type == "nltk_regexp_stemmer":
        stemmer = RegexpStemmer(**kwargs)
    else:
        stemmer = SnowballStemmer(**kwargs)

    return [stemmer.stem(word) for word in tokens]


def lemmatize(tokens: List[str], **kwargs: Any) -> List[str]:
    """Lemmatizes tokens using NLTK's WordNetLemmatizer

    Parameters
    ----------
    tokens : List[str]
        list of tokens containing words with various inflectional forms

    Other Parameters
    ----------------
    **kwargs : Any
        additional properties of the below lemmatizer:
          - nltk.WordNetLemmatizer

    Returns
    -------
    List[str]
        list of lemmatized tokens

    Examples
    --------
    >>> from contextpro.normalization import lemmatize
    >>> tokens =  ["I", "like", "driving", "a", "car"]
    >>> lemmatize(tokens, pos="v")
    ['I', 'like', 'drive', 'a', 'car']
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, **kwargs) for word in tokens]


def batch_lowercase_text(documents: List[str]) -> List[str]:
    """Converts sentences into lowercase.

    Parameters
    ----------
    documents : List[str]
        list of sentences with characters of arbitrary size

    Returns
    -------
    List[str]
        list of sentences with lowercased characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_lowercase_text
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> batch_lowercase_text(corpus)
    [
        "my name is dr. jekyll.",
        "his name is mr. hyde",
        "this guy's name is edward scissorhands",
        "and this is tom parker"
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [document.lower() for document in documents]


def batch_remove_non_ascii_characters(documents: List[str]) -> List[str]:
    """Removes non-ascii characters from sentences.

    Parameters
    ----------
    documents : List[str]
        list of sentences with non-ascii characters

    Returns
    -------
    List[str]
        list of sentences with removed non-ascii characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_non_ascii_characters
    >>> corpus = [
    ...     "https://sitebulb.com/Folder/øê.html?大学",
    ...     "J\xf6reskog bi\xdfchen Z\xfcrcher"
    ...     "This is a \xA9 but not a \xAE"
    ...     "fractions \xBC, \xBD, \xBE"
    ... ]
    >>> batch_remove_non_ascii_characters(corpus)
    [
        'https://sitebulb.com/Folder/.html?',
        'Jreskog bichen Zrcher',
        'This is a  but not a ',
        'fractions , , '
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [remove_non_ascii_characters(doc) for doc in documents]


def batch_replace_contractions(documents: List[str], **kwargs: bool) -> List[str]:
    """Expands contractions in sentences.

    Parameters
    ----------
    documents : List[str]
        list of sentences with contracted words

    Other Parameters
    ----------------
    **kwargs : bool
        additional properties of the below method:
          - contractions.fix()

    Returns
    -------
    List[str]
        list of sentences without contractions

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_replace_contractions
    >>> corpus = [
    ...     "I don't want to be rude, but you shouldn't do this",
    ...     "Do you think he'll pass his driving test?",
    ...     "I'll see you next week",
    ...     "I'm going for a walk"
    ... ]
    >>> batch_replace_contractions(corpus)
    [
        'I do not want to be rude, but you should not do this',
        'Do you think he will pass his driving test?',
        'I will see you next week',
        'I am going for a walk',
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [replace_contractions(doc, **kwargs) for doc in documents]


def batch_remove_stopwords(
    tokens: List[List[str]],
    custom_stopwords: List[str] = [],
) -> List[List[str]]:
    """Removes stopwords from nested token lists.

    Parameters
    ----------
    tokens : List[List[str]]
        nested token lists with stopwords included

    custom_stopwords: List[str], optional
        list of stopwords to remove from sentences, by default []

    Returns
    -------
    List[List[str]]
        nested token lists without stopwords

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_stopwords
    >>> corpus = [
    ...     ['My', 'name', 'is', 'Dr', 'Jekyll'],
    ...     ['His', 'name', 'is', 'Mr', 'Hyde'],
    ...     ['This', 'guy', 's', 'name', 'is', 'Edward', 'Scissorhands'],
    ...     ['And', 'this', 'is', 'Tom', 'Parker']
    ... ]
    >>> batch_remove_stopwords(corpus)
    [
        ['My', 'name', 'Dr', 'Jekyll'],
        ['His', 'name', 'Mr', 'Hyde'],
        ['This', 'guy', 'name', 'Edward', 'Scissorhands'],
        ['And', 'Tom', 'Parker']
    ]
    """
    if not _is_nested_string_list(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return [remove_stopwords(token_list, custom_stopwords) for token_list in tokens]


def batch_stem(
    tokens: List[List[str]],
    stemmer_type: Optional[str] = "nltk_porter_stemmer",
    num_workers: Optional[int] = None,
    **kwargs: Any,
) -> List[List[str]]:
    """Stems tokens in lists of tokens to their root (base) form in a
    concurrent manner.

    Parameters
    ----------
    tokens : List[List[str]]
        list of lists of tokens containing words with various
        inflectional forms

    stemmer_type : Optional[str], optional
        stemmer type which will be used to stem the tokens,
        by default "nltk_porter_stemmer"

        Allowed values:
          - nltk_porter_stemmer
          - nltk_lancaster_stemmer
          - nltk_regexp_stemmer
          - nltk_snowball_stemmer

    num_workers : Optional[int], optional
        number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : Any
        additional properties of the below stemmers:
          - nltk.PorterStemmer
          - nltk.LancasterStemmer
          - nltk.RegexpStemmer
          - nltk.SnowballStemmer

    Returns
    -------
    List[List[str]]
        list of lists of stemmed tokens

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_stem
    >>> corpus =  [
    ...     ["I", "like", "driving", "a", "car"],
    ...     ["I", "am", "going", "for", "a", "walk"],
    ...     ["Do", "you", "think", "this", "is", "doable"],
    ...     ["I", "have", "three", "bikes", "in", "two", "garages"]
    ... ]
    >>> batch_stem(
    ...    corpus,
    ...    stemmer_type="nltk_porter_stemmer",
    ...    num_workers=2
    ... )
    [
        ['I', 'like', 'drive', 'a', 'car'],
        ['I', 'am', 'go', 'for', 'a', 'walk'],
        ['Do', 'you', 'think', 'thi', 'is', 'doabl'],
        ['I', 'have', 'three', 'bike', 'in', 'two', 'garag']
    ]
    """
    if not _is_nested_string_list(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return cast(
        List[List[str]],
        _parallelize_func(
            stem,
            tokens,
            stemmer_type=stemmer_type,
            num_workers=num_workers,
            **kwargs,
        ),
    )


def batch_lemmatize(
    tokens: List[List[str]],
    num_workers: Optional[int] = None,
    **kwargs: Any,
) -> List[List[str]]:
    """Lemmatizes tokens in lists of tokens in a concurrent manner using
    NLTK WordNetLemmatizer.

    Parameters
    ----------
    tokens : List[List[str]]
        nested token lists containing tokens with various
        inflectional forms

    num_workers : Optional[int], optional
        number of logical processors to use, by default None (all)

    Other Parameters
    ----------------
    **kwargs : Any
        additional properties of the below lemmatizer:
          - nltk.WordNetLemmatizer

    Returns
    -------
    List[List[str]]
        nested token lists with lemmatized tokens

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_lemmatize
    >>> corpus =  [
    ...     ["I", "like", "driving", "a", "car"],
    ...     ["I", "am", "going", "for", "a", "walk"],
    ...     ["What", "are", "you", "doing"],
    ...     ["Where", "are", "you", "coming", "from"]
    ... ]
    >>> batch_lemmatize(corpus, num_workers=2, pos="v")
    [
        ['I', 'like', 'drive', 'a', 'car'],
        ['I', 'be', 'go', 'for', 'a', 'walk'],
        ['What', 'be', 'you', 'do'],
        ['Where', 'be', 'you', 'come', 'from']
    ]
    """
    if not _is_nested_string_list(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return cast(
        List[List[str]],
        _parallelize_func(lemmatize, tokens, num_workers=num_workers, **kwargs),
    )


def batch_remove_punctuation(documents: List[str]) -> List[str]:
    """Removes punctuation characters from all sentences.

    Parameters
    ----------
    documents : List[str]
        list of sentences which contain punctuation characters

    Returns
    -------
    List[str]
        list of sentences without punctuation characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_punctuation
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde!",
    ...     "Is his name Edward Scissorhands?",
    ...     "This is Tom-Parker!"
    ... ]
    >>> batch_remove_punctuation(corpus)
    [
        'My name is Dr Jekyll',
        'His name is Mr Hyde',
        'Is his name Edward Scissorhands',
        'This is TomParker'
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [remove_punctuation(doc) for doc in documents]


def batch_remove_numbers(documents: List[str]) -> List[str]:
    """Removes numbers from all sentences.

    Parameters
    ----------
    documents : List[str]
        list of sentences which contain numbers

    Returns
    -------
    List[str]
        list of sentences without numbers

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_numbers
    >>> corpus = [
    ...     "He is 12 years old.",
    ...     "His father has 3 cars",
    ...     "I have 3 computers",
    ...     "He earns 1000$ daily"
    ... ]
    >>> batch_remove_numbers(corpus)
    [
        'He is  years old.',
        'His father has  cars',
        'I have  computers',
        'He earns $ daily'
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [remove_numbers(doc) for doc in documents]


def batch_remove_whitespace(documents: List[str]) -> List[str]:
    r"""Removes whitespace characters from all sentences.

    Parameters
    ----------
    documents : List[str]
        list of sentences which contain whitespace characters

    Returns
    -------
    List[str]
        list of sentences without whitespace characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_whitespace
    >>> corpus = [
    ...     "He Has Not Been    in Touch for over a Month.",
    ...     "I Will See \r\nYou next Week",,
    ...     "I Am Hungry - Can We\t Eat Now, Please?",,
    ...     "It Is \r\nFreezing Outside!"
    ... ]
    >>> batch_remove_whitespace(corpus)
    [
        'He Has Not Been in Touch for over a Month.',
        'I Will See You next Week',
        'I Am Hungry - Can We Eat Now, Please?',
        'It Is Freezing Outside!',
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return [remove_whitespace(doc) for doc in documents]


def batch_convert_numerals_to_numbers(
    documents: List[str], num_workers: Optional[int] = None
) -> List[str]:
    """Replaces numerals with numbers in all sentences in a concurrent manner.

    Parameters
    ----------
    documents : List[str]
        list of sentences which contain numerals

    num_workers : Optional[int]
        number of logical processors to use, by default None (all)

    Returns
    -------
    List[str]
        list of sentences with numerals converted to numbers

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_convert_numerals_to_numbers
    >>> corpus = [
    ...     "A bunch of five",
    ...     "A picture is worth a thousand words",
    ...     "A stitch in time saves nine",
    ...     "Back to square one",
    ...     "Behind the eight ball",
    ...     "Between two stools",
    ... ]
    >>> batch_convert_numerals_to_numbers(corpus, num_workers=2)
    [
        'A bunch of 5',
        'A picture is worth a 1000 words',
        'A stitch in time saves 9',
        'Back to square 1',
        'Behind the 8 ball',
        'Between 2 stools',
    ]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[str],
        _parallelize_func(
            convert_numerals_to_numbers, documents, num_workers=num_workers
        ),
    )


__all__ = [
    "remove_stopwords",
    "remove_non_ascii_characters",
    "remove_punctuation",
    "remove_numbers",
    "remove_whitespace",
    "convert_numerals_to_numbers",
    "replace_contractions",
    "stem",
    "lemmatize",
    "batch_remove_non_ascii_characters",
    "batch_replace_contractions",
    "batch_remove_stopwords",
    "batch_stem",
    "batch_lemmatize",
    "batch_remove_punctuation",
    "batch_remove_numbers",
    "batch_remove_whitespace",
    "batch_convert_numerals_to_numbers",
]
