from myminions import update_yaml_file_content, load_yaml_file_content
from tempfile import TemporaryDirectory
from pathlib import Path


def test_update_yaml():
    with TemporaryDirectory() as tempdir:
        test_file = Path(tempdir).joinpath("test.yml")

        # adding nothing
        update_yaml_file_content(filepath=test_file, new_content=None)
        test_content = load_yaml_file_content(filepath=test_file)
        expected_content = {}
        assert str(test_content) == str(expected_content)

        # adding first level
        test_content = {"a": 1, "c": 3}
        update_yaml_file_content(filepath=test_file, new_content=test_content)
        test_content = load_yaml_file_content(filepath=test_file)
        assert str(test_content) == "{'a': 1, 'c': 3}"

        # adding local branch
        test_content={"a": {"b": 2}}
        update_yaml_file_content(filepath=test_file, new_content=test_content)
        test_content = load_yaml_file_content(filepath=test_file)
        assert str(test_content) == "{'a': {'b': 2}, 'c': 3}"

        # overriding local content
        test_content={"a": {"b": "two"}}
        update_yaml_file_content(filepath=test_file, new_content=test_content)
        test_content = load_yaml_file_content(filepath=test_file)
        assert str(test_content) == "{'a': {'b': 'two'}, 'c': 3}"

        # adding local content
        test_content={"a": {"d": 4}}
        update_yaml_file_content(filepath=test_file, new_content=test_content)
        test_content = load_yaml_file_content(filepath=test_file)
        assert str(test_content) == "{'a': {'b': 'two', 'd': 4}, 'c': 3}"
