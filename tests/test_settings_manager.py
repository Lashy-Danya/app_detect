import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from utils.settings_manager import SettingsManager


@pytest.fixture
def settings_file(tmpdir):
    """Fixture to create a temporary settings file."""
    settings_data = {"show_dialog_on_start": False}
    settings_file = Path(tmpdir) / "settings.json"
    with open(settings_file, "w") as file:
        json.dump(settings_data, file)
    return settings_file


def test_load_settings_existing_file(settings_file):
    """Test loading settings from an existing settings file."""
    manager = SettingsManager(filename=settings_file)
    expected = {"show_dialog_on_start": False}
    actual = manager.settings
    assert actual == expected, (
        f"Loading existing file failed, expected {expected}, got {actual}."
    )


def test_load_settings_new_file():
    """Test loading settings when the settings file doesn't exist."""
    with TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / "settings.json"
        manager = SettingsManager(filename=settings_file)
        expected = SettingsManager.DEFAULT_SETTINGS
        actual = manager.settings
        assert actual == expected, (
            f"Loading new file failed, expected {expected}, got {actual}."
        )


def test_get_setting(settings_file):
    """Test getting a specific setting."""
    manager = SettingsManager(filename=settings_file)
    expected = False
    actual = manager.get_setting("show_dialog_on_start")
    assert actual == expected, (
        f"Getting specific setting failed, expected {expected}, got {actual}."
    )


def test_set_setting(settings_file):
    """Test setting a specific setting."""
    manager = SettingsManager(filename=settings_file)
    manager.set_setting("show_dialog_on_start", True)
    expected = True
    actual = manager.get_setting("show_dialog_on_start")
    assert actual == expected, (
        f"Setting specific value failed, expected {expected}, got {actual}."
    )


def test_update_settings(settings_file):
    """Test updating multiple settings."""
    manager = SettingsManager(filename=settings_file)
    new_settings = {"theme": "dark", "font_size": 14}
    manager.update_settings(new_settings)
    expected = {"show_dialog_on_start": False, "theme": "dark", "font_size": 14}
    actual = manager.settings
    assert actual == expected, (
        f"Updating settings failed, expected {expected}, got {actual}."
    )


def test_error_handling_in_load_settings_with_corrupt_file():
    """Test error handling when the settings file contains invalid JSON."""
    with TemporaryDirectory() as tmpdir:
        corrupt_file = Path(tmpdir) / "settings.json"
        with open(corrupt_file, "w") as file:
            file.write("{not: 'JSON'}")
        
        manager = SettingsManager(filename=corrupt_file)
        expected = SettingsManager.DEFAULT_SETTINGS
        actual = manager.settings
        assert actual == expected, (
            f"Failed to load default settings on JSON decode error. "
            f"Got {actual}, expected {expected}."
        )


def test_save_functionality():
    """Test that settings are correctly saved to the file."""
    with TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / "settings.json"
        manager = SettingsManager(filename=settings_file)
        
        manager.set_setting("new_setting", True)
        
        with open(settings_file, 'r') as file:
            saved_settings = json.load(file)

        expected = True
        actual = saved_settings.get("new_setting")
        
        assert actual == expected, (
            f"Setting new_setting shoud be saved as '{expected}' "
            f"but was saved as: {actual}"
        )


def test_file_deletion_handling(settings_file):
    """Test handling of settings file deletion after initial load."""
    manager = SettingsManager(filename=settings_file)
    settings_file.unlink()
    expected = False
    actual = manager.get_setting("show_dialog_on_start")
    assert actual == expected, (
        f"File deletion handling failed, expected {expected}, got {actual}."
    )


def test_get_nonexistent_setting(settings_file):
    """Test getting a setting that doesn't exist."""
    manager = SettingsManager(filename=settings_file)
    expected = None
    actual = manager.get_setting("nonexistent_setting")
    assert actual == expected, (
        f"Getting nonexistent setting failed, expected {expected}, got {actual}."
    )
