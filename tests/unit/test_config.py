"""Test the configuration of the program."""

from unittest.mock import Mock, patch

import pytest
from ruamel.yaml.scanner import ScannerError

from mkdocs_newsletter.config import Config, ConfigError


# R0903: too few methods. C'est la vie!
class FileMarkMock:  # noqa: R0903
    """Mock of the ruamel FileMark object."""

    name: str = "mark"
    line: int = 1
    column: int = 1


def test_config_load(config: Config) -> None:
    """Loading the configuration from the yaml file works."""
    config.load()  # act

    assert config.data["verbose"] == "info"


@patch("mkdocs_newsletter.config.YAML")
def test_load_handles_wrong_file_format(yaml_mock: Mock, config: Config) -> None:
    """
    Given: A config file with wrong yaml format.
    When: configuration is loaded.
    Then: A ConfigError is returned.
    """
    yaml_mock.return_value.load.side_effect = ScannerError(
        "error",
        FileMarkMock(),
        "problem",
        FileMarkMock(),
    )

    with pytest.raises(ConfigError):
        config.load()


def test_load_handles_file_not_found(config: Config) -> None:
    """
    Given: An inexistent config file.
    When: configuration is loaded.
    Then: A ConfigError is returned.
    """
    config.config_path = "inexistent.yaml"

    with pytest.raises(ConfigError):
        config.load()


def test_save_config(config: Config) -> None:
    """Saving the configuration to the yaml file works."""
    config.data = {"a": "b"}

    config.save()  # act

    with open(config.config_path, "r") as file_cursor:
        assert "a:" in file_cursor.read()


def test_get_can_fetch_nested_items_with_dots(config: Config) -> None:
    """Fetching values of configuration keys using dot notation works."""
    config.data = {
        "first": {"second": "value"},
    }

    result = config.get("first.second")

    assert result == "value"


def test_config_can_fetch_nested_items_with_dictionary_notation(config: Config) -> None:
    """Fetching values of configuration keys using the dictionary notation works."""
    config.data = {
        "first": {"second": "value"},
    }

    result = config["first"]["second"]

    assert result == "value"


def test_get_an_inexistent_key_raises_error(config: Config) -> None:
    """If the key you're trying to fetch doesn't exist, raise a KeyError exception."""
    config.data = {
        "reports": {"second": "value"},
    }

    with pytest.raises(ConfigError):
        config.get("reports.inexistent")


def test_set_can_set_nested_items_with_dots(config: Config) -> None:
    """Setting values of configuration keys using dot notation works."""
    config.set("storage.type", "tinydb")  # act

    assert config.data["storage"]["type"] == "tinydb"
