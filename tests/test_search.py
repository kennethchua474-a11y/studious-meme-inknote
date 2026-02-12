from inknote.search import find_all


def test_find_single_match() -> None:
    text = "Hello world"
    matches = find_all(text, "world")
    assert matches == [(6, 11)]


def test_find_multiple_matches() -> None:
    text = "test test test"
    matches = find_all(text, "test")
    assert matches == [(0, 4), (5, 9), (10, 14)]


def test_case_insensitive_search() -> None:
    text = "Hello HELLO hello"
    matches = find_all(text, "hello", ignore_case=True)
    assert matches == [(0, 5), (6, 11), (12, 17)]


def test_case_sensitive_search() -> None:
    text = "Hello HELLO hello"
    matches = find_all(text, "hello", ignore_case=False)
    assert matches == [(12, 17)]


def test_empty_query_returns_empty_list() -> None:
    text = "some text"
    matches = find_all(text, "")
    assert matches == []
