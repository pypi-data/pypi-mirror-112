__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "1.1.1"
__all__ = ["walk_file_paths", "walk_folder_paths", "path_is_relative_to"]

import re
import sys
from pathlib import Path
from typing import Callable, Generator, Optional, Iterator, Union, List

APath = Union[str, Path]


def _39_relative_path(path_to_check: Path, other_path: Path) -> bool:
    """
    Returns the relative path of the *path to check* towards the *other path*.
    This method uses the ``pathlib.PurePath.is_relative_to`` method.

    Args:
        path_to_check:
            The path to check for being a sub path of the *other path*.

        other_path:
            The other path, which may be a parent path of the *path to check*.

    Returns:
        bool
    """
    return path_to_check.is_relative_to(other_path)


def _pre_39_relative_path(path_to_check: Path, other_path: Path) -> bool:
    """
    Returns the relative path of the *path to check* towards the *other path*.
    This method is the substitute for the ``pathlib.PurePath.is_relative_to``
    method, for python versions prior 3.9.

    Args:
        path_to_check:
            The path to check for being a sub path of the *other path*.

        other_path:
            The other path, which may be a parent path of the *path to check*.

    Returns:
        bool
    """
    search_pattern = "{}/.*".format(other_path)
    match_result = re.match(search_pattern, str(path_to_check))
    return match_result is not None


if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
    _path_is_relative_to = _39_relative_path
else:
    _path_is_relative_to = _pre_39_relative_path


def path_is_relative_to(path_to_check: Path, other_path: Path) -> bool:
    """
    Return whether or not this path is relative to the *other path*.

    Args:
        path_to_check:
            The path to check for being a sub path of the *other path*.

        other_path:
            The other path, which may be a parent path of the *path to check*.

    Returns:
        bool

    Examples:
        >>> from pathwalker import path_is_relative_to
        >>> from pathlib import Path
        >>> path_is_relative_to(path_to_check=Path("/a/b"), other_path=Path("/a"))
        True
        >>> path_is_relative_to(path_to_check=Path("/a/b"), other_path=Path("/c"))
        False
        >>> path_is_relative_to(path_to_check=Path("/ab"), other_path=Path("/a"))
        False
    """
    return _path_is_relative_to(path_to_check=path_to_check, other_path=other_path)


def _remove_sub_path_of(
    root_path_to_remain: Path, sorted_potential_sub_paths: List[Path]
) -> List[Path]:
    """
    Removes all sub paths or the *root path to remain* within the list of
    *sorted potential sub paths*.

    Args:
        root_path_to_remain:
            This path should remain within the list of *sorted potential sub paths*.

        sorted_potential_sub_paths:
            This is a list of potential sub paths.

    Returns:
        List[Path]

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> test_paths = (
        ...     "/a",
        ...     "/a/b",
        ...     "/a/b/c",
        ...     "/another",
        ...     "/another_one",
        ... )
        >>> cleared_sample_paths = _remove_sub_path_of(
        ...     sorted_potential_sub_paths = [Path(x) for x in test_paths],
        ...     root_path_to_remain = Path("/a/b"),
        ... )
        >>> doctest_iter_print(cleared_sample_paths)
        /a
        /a/b
        /another
        /another_one

        >>> cleared_sample_paths = _remove_sub_path_of(
        ...     sorted_potential_sub_paths = [Path(x) for x in test_paths],
        ...     root_path_to_remain = Path("/a"),
        ... )
        >>> doctest_iter_print(cleared_sample_paths)
        /a
        /another
        /another_one

        >>> cleared_sample_paths = _remove_sub_path_of(
        ...     sorted_potential_sub_paths = [Path(x) for x in test_paths],
        ...     root_path_to_remain = Path("/another"),
        ... )
        >>> doctest_iter_print(cleared_sample_paths)
        /a
        /a/b
        /a/b/c
        /another
        /another_one
    """
    remaining_paths = []
    for potential_sub_path in sorted_potential_sub_paths:
        is_the_searched_root_itself = potential_sub_path == root_path_to_remain
        if is_the_searched_root_itself:
            remaining_paths.append(root_path_to_remain)
            continue

        is_sub_path_of_the_searched_root = path_is_relative_to(
            path_to_check=potential_sub_path, other_path=root_path_to_remain
        )
        if is_sub_path_of_the_searched_root:
            continue

        remaining_paths.append(potential_sub_path)
    return remaining_paths


def _keep_resolved_root_paths(resolved_source_paths: List[Path]) -> List[Path]:
    """
    Keeps root paths within a list of paths. Sub paths are dropped.

    Args:
        resolved_source_paths:
            The paths must be resolved.

    Returns:
        List[Path]

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from pathlib import Path
        >>> sample_paths = (
        ...         "/tests/resources/bob/",
        ...         "/tests/resources/",
        ...         "/tests/resources/ariadne/",
        ...         "/another/root/",
        ...         "/another/root/here",
        ...     )
        >>> test_paths = [Path(x) for x in sample_paths]
        >>> cleared_sample_paths = _keep_resolved_root_paths(
        ...     resolved_source_paths=test_paths
        ... )
        >>> doctest_iter_print(cleared_sample_paths)
        /another/root
        /tests/resources

        Double entries need to be removed.
        >>> sample_paths = (
        ...         "/tests/resources/bob/",
        ...         "/tests/resources/bob/",
        ...         "/tests/resources/",
        ...         "/tests/resources/",
        ...         "/tests/resources/ariadne/",
        ...         "/tests/resources/ariadne/",
        ...         "/another/root/",
        ...         "/another/root/",
        ...         "/another/root/here",
        ...         "/another/root/here",
        ...     )
        >>> test_paths = [Path(x) for x in sample_paths]
        >>> cleared_sample_paths = _keep_resolved_root_paths(
        ...     resolved_source_paths=test_paths
        ... )
        >>> doctest_iter_print(cleared_sample_paths)
        /another/root
        /tests/resources
    """
    source_paths_without_doubles = list(set(resolved_source_paths))
    remaining_source_paths = list(sorted(source_paths_without_doubles))
    maximum_iterations = len(remaining_source_paths)
    for position in range(maximum_iterations):
        if position >= len(remaining_source_paths):
            break
        path_to_check = remaining_source_paths[position]
        remaining_source_paths = _remove_sub_path_of(
            sorted_potential_sub_paths=remaining_source_paths,
            root_path_to_remain=path_to_check,
        )
    return remaining_source_paths


def keep_root_paths(paths: List[APath]) -> List[Path]:
    """
    Keeps root paths within a list of paths. Sub paths are dropped.

    Notes:
        The purpose of this method is to get the minimum list of paths
        for a path recursion afterwards. This should avoid listing the
        items of sub paths or double entries within the list.



    Args:
        paths:
            Any paths; which will be resolved within this process.

    Returns:
        List[Path]:
            Resolved paths.

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from pathlib import Path

        The root should remain for later recursion.

        >>> sample_paths = (
        ...         "./tests/resources/foo",
        ...         "./tests/resources/bar",
        ...         "./tests/resources/",
        ...         "./tests/resources/foo/bar",
        ...         "./tests/resources/another_bar",
        ...     )
        >>> cleared_sample_paths = keep_root_paths(paths=sample_paths)
        >>> current_work_path = Path(".").resolve()
        >>> doctest_iter_print(
        ...     cleared_sample_paths,
        ...     edits_item=lambda x: x.relative_to(current_work_path)
        ... )
        tests/resources

        >>> sample_paths = (
        ...         "./tests/resources/foo",
        ...         "./tests/resources/bar",
        ...         "./tests/resources/foo/bar",
        ...         "./tests/resources/another_bar",
        ...     )
        >>> cleared_sample_paths = keep_root_paths(
        ...     paths=sample_paths
        ... )
        >>> current_work_path = Path(".").resolve()
        >>> doctest_iter_print(
        ...     cleared_sample_paths,
        ...     edits_item=lambda x: x.relative_to(current_work_path)
        ... )
        tests/resources/another_bar
        tests/resources/bar
        tests/resources/foo

        Double entries are removed from the list leaving single tree roots only.

        >>> samples = (
        ...         "./tests/resources/foo",
        ...         "./tests/resources/foo",
        ...         "./tests/resources/bar",
        ...         "./tests/resources/foo/bar",
        ...         "./tests/resources/foo/bar",
        ...         "./tests/resources/another_bar",
        ...         "./tests/resources/another_bar",
        ...     )
        >>> cleared_sample_paths = keep_root_paths(
        ...     paths=samples
        ... )
        >>> current_work_path = Path(".").resolve()
        >>> doctest_iter_print(
        ...     cleared_sample_paths,
        ...     edits_item=lambda x: x.relative_to(current_work_path)
        ... )
        tests/resources/another_bar
        tests/resources/bar
        tests/resources/foo

        Warnings:
            This method does resolve the paths. Non existing paths will not be dropped.
            Also this function will not raise a FileNotExist-Error for non existing
            paths.

        >>> samples = (
        ...         "./tests/resources/foo",
        ...         "./not/existing",
        ...         "./not/existing/either",
        ...     )
        >>> cleared_sample_paths = keep_root_paths(
        ...     paths=samples
        ... )
        >>> current_work_path = Path(".").resolve()
        >>> doctest_iter_print(
        ...     cleared_sample_paths,
        ...     edits_item=lambda x: x.relative_to(current_work_path)
        ... )
        not/existing
        tests/resources/foo


    """
    try:
        resolved_paths = [
            Path(source_path).resolve()
            for source_path in paths
            if source_path is not None
        ]
    except TypeError as e:
        original_error = e.args[0]
        raise TypeError(
            "All provided paths are expected to be a {}".format(original_error[9:])
        )

    return _keep_resolved_root_paths(resolved_source_paths=resolved_paths)


def _get_path_generator(
    root_path: Path, recursive: bool = False
) -> Callable[[str], Generator]:
    searched_root_path = Path(root_path)
    if recursive:
        return searched_root_path.rglob
    else:
        return searched_root_path.glob


def _get_filter_pattern(pattern: Optional[str]):
    retrieve_all_paths = pattern is None
    if retrieve_all_paths:
        return "*"
    return pattern


def walk_folder_paths(
    root_path: APath, filter_pattern: Optional[str] = None, recursive: bool = False
) -> Iterator[Path]:
    """
    Yields only paths of directories.

    Args:
        root_path(Path):
            Root path to walk thourgh.

        filter_pattern(str):
            Unix path pattern for filtering retrieved paths.

        recursive(bool:
            Returns also paths of all sub folders.

    Yields:
        Path

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from pathwalker import walk_folder_paths
        >>> found_folders = sorted(
        ...     walk_folder_paths("./tests", filter_pattern = "[!._]*"),
        ...     key=lambda x: str(x)
        ... )
        >>> doctest_iter_print(found_folders)
        tests/resources

        >>> found_folders = sorted(
        ...     walk_folder_paths("./tests", filter_pattern = "[!._]*", recursive=True),
        ...     key=lambda x: str(x)
        ... )
        >>> doctest_iter_print(found_folders)
        tests/resources
        tests/resources/another_bar
        tests/resources/bar
        tests/resources/foo
        tests/resources/foo/bar


    """
    path_generator = _get_path_generator(root_path=root_path, recursive=recursive)
    used_filter_pattern = _get_filter_pattern(filter_pattern)

    for child_path in path_generator(used_filter_pattern):
        if child_path.is_file():
            continue
        yield child_path


def walk_file_paths(
    root_path: APath, filter_pattern: Optional[str] = None, recursive: bool = False
) -> Generator[Path, None, None]:
    """
    Yields only file paths.

    Args:
        root_path(Path):
            Root path to walk through.

        filter_pattern(str):
            Unix path pattern for filtering retrieved paths.

        recursive(bool:
            Returns also paths of all sub folders.

    Yields:
        Path

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from pathwalker import walk_file_paths
        >>> found_files = sorted(
        ...     walk_file_paths("tests/.", filter_pattern = "[!._]*.py", recursive=True),
        ...     key=lambda x: str(x)
        ... )
        >>> doctest_iter_print(found_files)
        tests/path_test.py
        tests/resources/foo.py
        tests/test_common_paths.py

    """
    path_generator = _get_path_generator(root_path=root_path, recursive=recursive)
    used_filter_pattern = _get_filter_pattern(filter_pattern)

    for child_path in path_generator(used_filter_pattern):
        if child_path.is_dir():
            continue
        yield child_path
