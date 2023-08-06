from typing import List

from contextpro._processing import _is_nested_string_list, _is_string_list


def get_ngrams(tokens: List[str], ngram_size: int = 1) -> List[str]:
    """Prepare n-grams from the provided list of tokens.

    Parameters
    ----------
    tokens : List[str]
        list of tokens

    ngram_size: int
        size of ngrams to return, by default 1 - unigrams

    Returns
    -------
    List[List[str]]
        list of ngrams

    Raises
    ------
    ValueError
        if 'tokens' provided is not a list of strings

    Examples
    --------
    >>> from contextpro.feature_extraction import get_ngrams
    >>> tokens = ["my", "name", "is", "dr", "jekyll"]
    >>> get_ngrams(tokens, ngram_size=2)
    ["my name", "name is", "is spiderman"]
    """
    if not _is_string_list(tokens):
        raise ValueError("'tokens' should be a list of strings")

    ngrams = []
    for num in range(0, len(tokens)):
        ngram = " ".join(tokens[num : num + ngram_size])
        ngrams.append(ngram)
    return [ngram for ngram in ngrams if len(ngram.split(" ")) == ngram_size]


def batch_get_ngrams(tokens: List[List[str]], ngram_size: int = 1) -> List[List[str]]:
    """Prepare n-grams from the provided list of token lists.

    Parameters
    ----------
    tokens : List[List[str]]
        list of token lists, each representing single document

    ngram_size: int
        size of ngrams to return, by default 1 - unigrams

    Returns
    -------
    List[List[str]]
        list of nested ngram lists

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.feature_extraction import batch_get_ngrams
    >>> tokens = [
    ...     ["my", "name", "is", "spiderman"],
    ...     ["she", "lives", "in", "australia"],
    ... ]
    >>> batch_get_ngrams(tokens, ngram_size=2)
    [
        ["my name", "name is", "is spiderman"],
        ["she lives", "lives in", "in australia"],
    ]
    """
    if not _is_nested_string_list(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return [get_ngrams(token_list, ngram_size=ngram_size) for token_list in tokens]
