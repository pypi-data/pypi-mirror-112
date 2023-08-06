import sys
from pathlib import Path

import pytest

from pathwalker import _keep_resolved_root_paths, _remove_sub_path_of, keep_root_paths


def _lists_are_equal(outcome, expected_outcome):
    expected_outcome_items = set(expected_outcome)
    test_difference = expected_outcome_items.difference(outcome)
    return len(test_difference) == 0


def test_39_path_is_relative_to():
    if sys.version[0] == 3 and sys.version_info[1] >= 9:
        from pathwalker import _39_relative_path

        assert _39_relative_path(path_to_check=Path("/a/b"), other_path=Path("/a"))
        assert not _39_relative_path(path_to_check=Path("/a/b"), other_path=Path("/c"))
        assert not _39_relative_path(path_to_check=Path("/ab"), other_path=Path("/a"))


def test_pre_39_path_is_relative_to():
    if sys.version[0] == 3 and sys.version_info[1] >= 9:
        from pathwalker import _pre_39_relative_path

        assert _pre_39_relative_path(path_to_check=Path("/a/b"), other_path=Path("/a"))
        assert _pre_39_relative_path(
            path_to_check=Path("/a/b/c/d"), other_path=Path("/a/b")
        )
        assert not _pre_39_relative_path(
            path_to_check=Path("/a/b"), other_path=Path("/c")
        )
        assert not _pre_39_relative_path(
            path_to_check=Path("/ab"), other_path=Path("/a")
        )


def test_remove_sub_path_of_a_tree():
    """

    >>> from doctestprinter import doctest_iter_print
    >>> doctest_iter_print(test_remove_sub_path_of_a_tree())
    tests/resources
    """
    samples = (
        "./tests/resources/",
        "./tests/resources/foo/bar",
    )
    test_paths = [Path(x).resolve() for x in sorted(samples)]
    expected_path = Path("./tests/resources/").resolve()

    resulting_output = _remove_sub_path_of(
        root_path_to_remain=expected_path, sorted_potential_sub_paths=test_paths
    )

    workdir = Path(".").resolve()
    return [total_path.relative_to(workdir) for total_path in resulting_output]


def test_remove_sub_path_of():
    samples = (
        "./tests/resources/",
        "./tests/resources/foo",
        "./tests/resources/bar",
        "./tests/resources/foo/bar",
        "./tests/resources/another_bar",
    )

    test_paths = [Path(x).resolve() for x in sorted(samples)]
    expected_path = Path("./tests/resources/").resolve()

    resulting_output = _remove_sub_path_of(
        root_path_to_remain=expected_path, sorted_potential_sub_paths=test_paths
    )
    assert len(resulting_output) == 1, "There should only be one resulting path left."
    assert resulting_output[0] == expected_path


def test_keep_resolved_root_paths():
    sample = ("/a", "/b", "/c")
    test_paths = [Path(x) for x in sample]
    output_paths = _keep_resolved_root_paths(test_paths)
    expected_outcome = [Path(x) for x in sample]
    assert _lists_are_equal(output_paths, expected_outcome)

    sample = ("/a",)
    test_paths = [Path(x) for x in sample]
    output_paths = _keep_resolved_root_paths(test_paths)
    expected_outcome = [Path(x) for x in sample]
    assert _lists_are_equal(output_paths, expected_outcome)

    sample = ("",)
    test_paths = [Path(x) for x in sample]
    output_paths = _keep_resolved_root_paths(test_paths)
    expected_outcome = [Path(x) for x in sample]
    assert _lists_are_equal(output_paths, expected_outcome)

    sample = (
        "/a",
        "/b",
        "/",
    )
    test_paths = [Path(x) for x in sample]
    output_paths = _keep_resolved_root_paths(test_paths)
    expected_outcome = [Path("/")]
    assert _lists_are_equal(output_paths, expected_outcome)


def test_keep_root_paths():
    resulting_output = keep_root_paths([""])
    expected_path = Path("").resolve()
    assert len(resulting_output) == 1, "There should only be one resulting path left."
    assert resulting_output[0] == expected_path

    resulting_output = keep_root_paths([])
    assert len(resulting_output) == 0

    resulting_output = keep_root_paths([None])
    assert len(resulting_output) == 0

    with pytest.raises(TypeError):
        keep_root_paths(keep_root_paths([1]))

def test_keep_root_paths_with_non_existing():
    resulting_output = keep_root_paths(["/this/doesn't/exists"])
    expected_output = [Path("/this/doesn't/exists")]
    non_existing_paths_are_not_dropped = resulting_output[0] == expected_output[0]
    assert non_existing_paths_are_not_dropped
