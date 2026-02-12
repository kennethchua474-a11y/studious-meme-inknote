from __future__ import annotations

from typing import List, Tuple

Match = Tuple[int, int]


def find_all(
    text: str,
    query: str,
    *,
    ignore_case: bool = False,
) -> List[Match]:
    """
    Finds all occurences of `query` in `text`.

    Returns a list of (start_index, end_index) tuples.
    """

    if not query:
        return []

    if ignore_case:
        text_to_search = text.lower()
        query_to_search = query.lower()
    else:
        text_to_search = text
        query_to_search = query

    matches: List[Match] = []
    start = 0

    while True:
        index = text_to_search.find(query_to_search, start)
        if index == -1:
            break

        end = index + len(query)
        matches.append((index, end))
        start = end

    return matches
