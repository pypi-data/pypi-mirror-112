"""This module contains functions used for text data tokenization."""

from typing import List, Optional, cast

import nltk

from contextpro._processing import _is_string_list, _parallelize_func


def batch_tokenize_text(
    documents: List[str],
    tokenizer_method: Optional[str] = "nltk_word_tokenizer",
    num_workers: Optional[int] = None,
    **kwargs,
) -> List[List[str]]:
    r"""Tokenizes sentences in a concurrent manner.

    Parameters
    ----------
    documents : List[str]
        list of sentences to tokenize

    tokenizer_method : Optional[str]
        tokenization method which will be used to tokenize the sentences
        by default "nltk_word_tokenizer".

        Allowed values:
          - nltk_word_tokenizer
          - nltk_regexp_tokenizer

    num_workers : Optional[int], optional
        number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : additional properties of the below methods:

      - nltk.word_tokenize()
      - nltk.regexp_tokenize()

    Returns
    -------
    List[List[str]]
        nested lists containing tokens

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.tokenization import batch_tokenize_text
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> batch_tokenize_text(
    ...     corpus,
    ...     tokenizer_method="nltk_regexp_tokenizer",
    ...     pattern=r"\b[^\d\W]+\b",
    ...     gaps=False,
    ...     num_workers=2
    ... )
    [['My', 'name', 'is', 'Dr', 'Jekyll'],
     ['His', 'name', 'is', 'Mr', 'Hyde'],
     ['This', 'guy', 's', 'name', 'is', 'Edward', 'Scissorhands'],
     ['And', 'this', 'is', 'Tom', 'Parker']]
    """
    if not _is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[List[str]],
        _parallelize_func(
            tokenize_text,
            documents,
            tokenizer_method=tokenizer_method,
            num_workers=num_workers,
            **kwargs,
        ),
    )


def tokenize_text(
    document: str,
    tokenizer_method: Optional[str] = "nltk_word_tokenizer",
    **kwargs,
) -> List[str]:
    r"""Convert sentence into a list of tokens.

    Parameters
    ----------
    documents : str
        sentence to tokenize

    tokenizer_method : Optional[str]
        tokenization method which will be used to tokenize the sentence
        by default "nltk_word_tokenizer".

        Allowed values:
          - nltk_word_tokenizer
          - nltk_regexp_tokenizer

    Other Parameters
    ----------------
    **kwargs : additional properties of the below methods:

      - nltk.word_tokenize()
      - nltk.regexp_tokenize()

    Returns
    -------
    List[str]
        list of tokens

    Examples
    --------
    >>> from contextpro.tokenization import tokenize_text
    >>> sentence = "My name is Dr. Jekyll."
    >>> tokenize_text(
    ...     corpus,
    ...     tokenizer_method="nltk_regexp_tokenizer",
    ...     pattern=r"\b[^\d\W]+\b",
    ...     gaps=False,
    ... )
    ['My', 'name', 'is', 'Dr', 'Jekyll']
    """
    if tokenizer_method == "nltk_word_tokenizer":
        tokens = nltk.word_tokenize(document, **kwargs)
    elif tokenizer_method == "nltk_regexp_tokenizer":
        tokens = nltk.regexp_tokenize(document, **kwargs)
    return cast(List[str], tokens)


__all__ = ["tokenize_text", "batch_tokenize_text"]
