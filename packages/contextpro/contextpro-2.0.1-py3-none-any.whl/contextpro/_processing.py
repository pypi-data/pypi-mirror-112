"""This module contains definitions of custom types used within the
library and some utility functions for data validation and batch
processing."""

from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Iterable, List, Optional, Union


def _parallelize_func(
    func: Callable[..., Any],
    iterable: Iterable[Any],
    num_workers: Optional[int] = None,
    **kwargs,
) -> Iterable[Any]:
    """Run provided function using multiple cores.

    Parameters
    ----------
    func : Callable[..., Any]
        Python function

    iterable : Iterable[Any]
        Iterable of elements to process

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    Iterable[Any]
        Iterable of processed elements
    """
    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(func, item, **kwargs) for item in iterable]
        for future in futures:
            results.append(future.result())
    return results


def _is_string_list(string_list: Union[List[str], List[List[str]]]) -> bool:
    """Check whether the argument is a list of strings.

    Parameters
    ----------
    string_list : List[str]
        List of strings

    Returns
    -------
    bool
        True if argument is a list of strings, False otherwise
    """
    if isinstance(string_list, list) and all(
        isinstance(element, str) for element in string_list
    ):
        return True
    else:
        return False


def _is_nested_string_list(nested_string_lists: List[List[str]]) -> bool:
    """Check whether the argument is a list of nested string lists.

    Parameters
    ----------
    nested_string_lists : List[List[str]]
        List of lists of strings

    Returns
    -------
    bool
        True if argument is a list of nested string lists, False otherwise
    """
    if isinstance(nested_string_lists, list) and all(
        _is_string_list(string_list) for string_list in nested_string_lists
    ):
        return True
    else:
        return False
