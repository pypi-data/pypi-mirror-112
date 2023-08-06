__all__ = [
    "add_handler_once_per_session",
    "APath",
    "handler_writing_logs_onto_console",
    "load_yaml_file_content",
    "remove_path_or_tree",
    "try_decoding_potential_text_content",
    "update_yaml_file_content",
    "get_piped_command_line_arguments",
    "ENCODING_FORMAT_TRYOUTS",
    "copy_tree",
    "list_tree_relatively",
    "file_trees_have_equal_paths",
]

import io
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Union, List, Optional, Iterable, Generator
import yaml

# create LOGGER with this namespace's name
from pathwalker import path_is_relative_to, walk_folder_paths, walk_file_paths

_logger = logging.getLogger("myminions")
_logger.setLevel(logging.ERROR)
# create console handler and set level to debug
handler_writing_logs_onto_console = logging.StreamHandler()
# add formatter to ch
handler_writing_logs_onto_console.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(funcName)s "
        "- %(lineno)s - %(levelname)s - %(message)s"
    )
)


APath = Union[str, Path, os.PathLike]


def add_handler_once_per_session(handler):
    """
    Avoid declaring the same handler multiple times, leading to multiple
    outputs of the same message.

    Args:
        handler:
            The handler to add.
    """

    def _same_handler_type_is_already_registered(
        searched_handler_type, logger: logging.Logger
    ) -> bool:
        for registered_handlers_of_this_session in logger.handlers:
            if isinstance(registered_handlers_of_this_session, searched_handler_type):
                return True
        return False

    global _logger
    current_handler = type(handler)
    if not _same_handler_type_is_already_registered(current_handler, _logger):
        _logger.addHandler(handler)


# Using the method for this module.
add_handler_once_per_session(handler_writing_logs_onto_console)


def _iter_split_piped_arguments(arguments: List[str]) -> Generator[str, None, None]:
    """
    Examples:
        >>> list(_iter_split_piped_arguments(["a", "", "b", ""]))
        ['a', 'b']

    Args:
        piped_argument_content(List[str]):
            Split content of the pipe.

    Yields:
        str
    """
    for argument in arguments:
        if argument == "":
            continue
        yield argument


def get_piped_command_line_arguments(
    preliminary_args: Optional[Iterable] = None,
) -> List:
    """
    Grabs the piped arguments from the sys.stdin and removes empty strings from
    the arguments. The piped arguments will extent supplied *prelimiary arguments*.

    Args:
        preliminary_args(List):
            These arguments will be put in front.

    Returns:
        List
    """
    if not isinstance(preliminary_args, Iterable):
        raise TypeError(
            "preliminary_args must be an Iterable. "
            "Got type of '{}' instead.".format(type(preliminary_args))
        )

    pipe_was_not_empty = not sys.stdin.isatty()
    if pipe_was_not_empty:
        input_stream = sys.stdin
        if not isinstance(input_stream, io.TextIOWrapper):
            raise TypeError(
                "The stream input was not a text file. "
                "Got type of '' instead.".format(type(input_stream))
            )
        split_piped_arguments = input_stream.read().split("\n")
        piped_arguments = [
            potential_path
            for potential_path in _iter_split_piped_arguments(split_piped_arguments)
        ]
    else:
        piped_arguments = []

    if preliminary_args is None:
        args_in_front = []
    else:
        args_in_front = list(preliminary_args)
    return args_in_front + piped_arguments


def overlap_dict_branches(target_branch: dict, source_branch: dict) -> dict:
    """
    Overlaps to dictionaries with each other. This method does apply changes
    to the given dictionary instances.

    Args:
        target_branch(dict):
            Root where the new branch should be put.

        source_branch(dict):
            New data to be put into the source_branch.

    Raises:
        TypeError:
            if target_branch is not a dictionary.

    Examples:
        >>> overlap_dict_branches(
        ...     target_branch={"a": 1, "b": {"de": "ep"}},
        ...     source_branch={"b": {"de": {"eper": 2}}}
        ... )
        {'a': 1, 'b': {'de': {'eper': 2}}}
        >>> overlap_dict_branches(
        ...     target_branch={},
        ...     source_branch={"ne": {"st": "ed"}}
        ... )
        {'ne': {'st': 'ed'}}
        >>> overlap_dict_branches(
        ...     target_branch={"ne": {"st": "ed"}},
        ...     source_branch={}
        ... )
        {'ne': {'st': 'ed'}}
        >>> overlap_dict_branches(
        ...     target_branch={"ne": {"st": "ed"}},
        ...     source_branch={"ne": {"st": "ed"}}
        ... )
        {'ne': {'st': 'ed'}}

        >>> overlap_dict_branches(
        ...     target_branch={}, source_branch=None
        ... )
        {}

    """
    if not isinstance(source_branch, dict):
        return target_branch
    if not isinstance(target_branch, dict):
        raise TypeError("target_branch needs to be a dictionary.")
    for key, newItem in source_branch.items():
        if key not in target_branch:
            target_branch[key] = newItem
        elif isinstance(target_branch[key], dict):
            target_branch[key] = overlap_dict_branches(target_branch[key], newItem)
        else:
            target_branch[key] = newItem
    return target_branch


def load_yaml_file_content(filepath: APath, default: dict = None) -> dict:
    """
    Load the yaml file content returning the parsed result.

    Args:
        filepath(Path):
            The file path of the yaml file, which should be loaded and parsed.

        default(dict):
            The default dict, which will be returned if the filepath doesn't
            exist or the files content is 'None'.

    Examples:
        >>> load_yaml_file_content("file/not/existing.yml", default={"doc": "test"})
        {'doc': 'test'}

        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tempdir:
        ...     test_filepath = Path(tempdir).joinpath("test.yml")
        ...     test_filepath.touch()
        ...     empty_test_content = load_yaml_file_content(
        ...         filepath=test_filepath, default={}
        ...     )
        ...     print(empty_test_content)
        {}

    Returns:
        dict
    """
    assert filepath is not None, "filepath cannot be 'None'"
    assert default is None or isinstance(default, dict), "'default' must be a dict."

    try:
        yml_filepath = Path(filepath)
    except TypeError:
        raise ValueError("A valid filepath needs to be supplied. 'None' is not valid.")

    if not yml_filepath.exists():
        no_user_default_was_given_then_log_error = default is None
        if no_user_default_was_given_then_log_error:
            _logger.error(
                "'{}' was not found and therefore not loaded. "
                "An empty dict was returned instead. "
                "To turn this message off, either provide only existing file paths "
                "or explicitely define the argument `default` with an returning value."
                "".format(yml_filepath)
            )
            return {}
        else:
            if not isinstance(default, dict):
                raise TypeError("'default' must be a dictionary.")
            return default

    with open(yml_filepath, "rb") as yml_file:
        setup_binary_content = yml_file.read()
    upload_config_text = try_decoding_potential_text_content(setup_binary_content)
    external_setup = yaml.load(upload_config_text, Loader=yaml.SafeLoader)

    if external_setup is None:
        return default

    return external_setup


def update_yaml_file_content(filepath: APath, new_content: dict):
    """
    Updates the existing content of a yaml file with the *new content*. If the
    file does not exist a new file will be created.

    Notes:
        Overlapping values of new_content will override existing entries.
        Used method for merging the existing file content with the *new content*
        is :func:`myminions.overlap_dict_branches`.

    Examples:
        >>> from tempfile import TemporaryDirectory
        >>> from pathlib import Path
        >>> with TemporaryDirectory() as tempdir:
        ...     temporary_filepath = Path(tempdir, "test.yml")
        ...     update_yaml_file_content(
        ...         temporary_filepath, {"a": 1, "b": {"de": "ep"}}
        ...     )
        ...     update_yaml_file_content(
        ...         temporary_filepath, {"b": {"de": {"eper": 2}}}
        ...     )
        ...     print(load_yaml_file_content(temporary_filepath))
        {'a': 1, 'b': {'de': {'eper': 2}}}

    Args:
        filepath(APath):
            The file path of the yaml file, which should be loaded and parsed.

        new_content(dict):
            The new content, which will be updated into the existing content.
            It should be parsable by pyyaml.
    """
    current_file_content = load_yaml_file_content(filepath, default={})
    updated_content = overlap_dict_branches(current_file_content, new_content)
    with open(filepath, "w") as yaml_file:
        yaml.dump(updated_content, yaml_file)


ENCODING_FORMAT_TRYOUTS = ["utf-8", "latin-1", "iso-8859-1", "windows-1252"]


def try_decoding_potential_text_content(
    byte_like_content, encoding_format_tryouts: List[str] = None
) -> str:
    """
    Tries to decode the given byte-like content as a text using the given
    encoding format types.

    Notes:
        The first choice is 'utf-8', but in case of different OS are involved,
        some json files might been created using a different encoding, leading
        to errors. Therefore this methods tries the encondings listed in
        *myminions.ENCODING_FORMAT_TRYOUTS* by default.

    Examples:
        >>> from myminions import try_decoding_potential_text_content
        >>> sample = '{"a": "test", "json": "string with german literals äöüß"}'
        >>> sample_latin_1 = sample.encode(encoding="latin-1")
        >>> sample_latin_1
        b'{"a": "test", "json": "string with german literals \xe4\xf6\xfc\xdf"}'
        >>> try_decoding_potential_text_content(sample_latin_1)
        '{"a": "test", "json": "string with german literals äöüß"}'
        >>> sample_windows = sample.encode(encoding="windows-1252")
        >>> sample_windows
        b'{"a": "test", "json": "string with german literals \xe4\xf6\xfc\xdf"}'
        >>> try_decoding_potential_text_content(sample_windows)
        '{"a": "test", "json": "string with german literals äöüß"}'

    Args:
        byte_like_content:
            The text as byte-like object, which should be decoded.

        encoding_format_tryouts: List[str]:
            Formats in which the text might be encoded.

    Raises:
        UnicodeDecodeError

    Returns:
        str:
            Hopefully a proper decoded text.
    """
    if encoding_format_tryouts is None:
        encoding_format_tryouts = ENCODING_FORMAT_TRYOUTS
    return _try_decoding_content(byte_like_content, encoding_format_tryouts)


def _try_decoding_content(byte_like_content, encoding_format_tryouts: List[str]) -> str:
    """
    Tries to decode the given byte-like content as a text using the given
    encoding format types.

    Args:
        byte_like_content:
            The text as byte-like object, which should be decoded.

        encoding_format_tryouts: List[str]:
            Formats in which the text might be encoded.

    Raises:
        UnicodeDecodeError

    Returns:
        str:
            Hopefully a proper decoded text.
    """

    def _try_decoding_content_upon_error(
        byte_like_content, encoding_format_tryouts, last_error=None
    ):
        """
        Tries to encode the text until success. If every encoding format
        failed, then the last UnicodeDecodeError is raised.

        Args:
        byte_like_content:
            The text as byte-like object, which should be decoded.

        encoding_format_tryouts: List[str]:
            Formats in which the text might be encoded.

        last_error(optional):
            Last caught error.

        Returns:
            str:
                Hopefully a proper decoded text.
        """
        no_tried_format_succeeded = len(encoding_format_tryouts) == 0
        if no_tried_format_succeeded:
            raise last_error

        encoding_format = encoding_format_tryouts.pop(0)
        try:
            decoded_content = byte_like_content.decode(encoding_format)
            return decoded_content
        except UnicodeDecodeError as e:
            return _try_decoding_content_upon_error(
                byte_like_content, encoding_format_tryouts, e
            )

    format_tryouts = encoding_format_tryouts.copy()
    decoded_content = _try_decoding_content_upon_error(
        byte_like_content, format_tryouts
    )
    return decoded_content


def list_tree_relatively(root_path: Path) -> List[Path]:
    """
    List all paths within the *root_path* relative to it.

    Args:
        root_path:
            The root path which paths shall be listed.

    Returns:
        List[Path]

    Examples:

        >>> from doctestprinter import doctest_iter_print
        >>> samples = list_tree_relatively(root_path="./tests/resources")
        >>> doctest_iter_print(sorted(samples, key=lambda x:str(x)))
        resources_index.md
        sample-1
        sample-1/.hidden
        sample-1/file-1.txt
        sample-1/file-2.csv

    """
    root_path = Path(root_path)
    relative_file_paths = []
    for filepath in root_path.rglob("*"):
        relative_filepath = filepath.relative_to(root_path)
        relative_file_paths.append(relative_filepath)
    return relative_file_paths


def file_trees_have_equal_paths(
    expected_tree_path: APath, target_tree_path: APath
) -> bool:
    """
    Checks if two file trees are structured equally on basis of their filepaths.
    The content of these files is not checked within this function.

    Args:
        expected_tree_path:
            The tree path which paths are expected.

        target_tree_path:
            The tree path to check against the expected tree path.

    Returns:
        bool

    Examples:
        >>> file_trees_have_equal_paths(
        ...     expected_tree_path="./tests/resources",
        ...     target_tree_path="./tests/resources"
        ... )
        True

        >>> file_trees_have_equal_paths(
        ...     expected_tree_path="./tests/resources",
        ...     target_tree_path="./tests"
        ... )
        False

    """
    expected_content = list_tree_relatively(root_path=expected_tree_path)
    target_content = list_tree_relatively(root_path=target_tree_path)

    difference_of_trees = set(expected_content).difference(target_content)

    difference_is_empty_then_both_are_equal = len(difference_of_trees) == 0
    if difference_is_empty_then_both_are_equal:
        return True
    return False


def copy_tree(source_path: APath, destination_path: APath):
    """
    Copies the content of the source tree to the destination.

    Args:
        source_path:


        destination_path:

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as temp_dir:
        ...     target_path = Path(temp_dir).joinpath("test")
        ...     copy_tree("./tests/resources", target_path)
        ...     success_of_copy = file_trees_have_equal_paths(
        ...         expected_tree_path="./tests/resources",
        ...         target_tree_path=target_path
        ...     )
        ...     relative_test_files = list_tree_relatively(target_path)
        >>> print("Copying trees was successful:", success_of_copy)
        Copying trees was successful: True
        >>> doctest_iter_print(sorted(relative_test_files, key=lambda x: str(x)))
        resources_index.md
        sample-1
        sample-1/.hidden
        sample-1/file-1.txt
        sample-1/file-2.csv
    """
    source_path = Path(source_path).resolve()
    destination_root_path = Path(destination_path)

    if not destination_root_path.exists():
        destination_root_path.mkdir(parents=True)

    folder_walker = walk_folder_paths(source_path, filter_pattern="*", recursive=True)
    for folder_path in folder_walker:
        sub_path = folder_path.relative_to(source_path)
        destination_dir = destination_root_path.joinpath(sub_path)
        if not destination_dir.exists():
            destination_dir.mkdir()

    file_walker = walk_file_paths(source_path, filter_pattern="*", recursive=True)
    for filepath in file_walker:
        resolved_filepath = filepath.resolve()
        sub_path = resolved_filepath.relative_to(source_path)
        destination_filepath = destination_root_path.joinpath(sub_path)
        shutil.copy2(resolved_filepath, destination_filepath)


def remove_path_or_tree(root_path_to_remove: APath):
    """
    Removes the path, either if it is just a path or a whole path tree.

    Examples:
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tempdir:
        ...     target_path = Path(tempdir).joinpath("test")
        ...     copy_tree("./tests/resources", target_path)
        ...     copy_was_successful = target_path.joinpath("sample-1/.hidden").exists()
        ...     remove_path_or_tree(target_path)
        ...     removing_the_path_was_successful = not target_path.exists()
        >>> print("Copying the tree was successful:", copy_was_successful)
        Copying the tree was successful: True
        >>> print("Removing the tree was successful:", removing_the_path_was_successful)
        Removing the tree was successful: True

    Raises:
        TypeError:
            If somethink else is providen than the expected a str, bytes or
            os.PathLike object.

    Args:
        root_path_to_remove(APath):
            Root path to remove.

    Returns:
        bool
    """
    root_path_to_remove = Path(root_path_to_remove)
    it_is_just_a_file_then_remove_it_and_exit = root_path_to_remove.is_file()
    if it_is_just_a_file_then_remove_it_and_exit:
        root_path_to_remove.unlink()
        return

    shutil.rmtree(str(root_path_to_remove))
