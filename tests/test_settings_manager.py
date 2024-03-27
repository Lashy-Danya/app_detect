import pytest

from pathlib import Path

from app.settings_manager import SettingsManager

# Fixture to clean up the settings file before and after the tests
@pytest.fixture
def clean_settings_file():
    filename = Path("test_settings.json")
    if filename.exists():
        filename.unlink()  # Remove the file if it exists
    yield
    if filename.exists():
        filename.unlink()  # Ensure the file is deleted after the test

def test_settings_manager_initialization(clean_settings_file):
    # Test if the SettingsManager initializes with the default settings
    manager = SettingsManager(filename="test_settings.json")
    assert manager.get_setting("show_dialog_on_start") is True

def test_set_and_get_setting(clean_settings_file):
    # Test setting and getting a value
    manager = SettingsManager(filename="test_settings.json")
    manager.set_setting("show_dialog_on_start", False)
    assert manager.get_setting("show_dialog_on_start") is False

def test_update_settings(clean_settings_file):
    # Test updating settings
    manager = SettingsManager(filename="test_settings.json")
    new_settings = {
        "show_dialog_on_start": False,
        "new_setting": "value"
    }
    manager.update_settings(new_settings)
    assert manager.get_setting("show_dialog_on_start") is False
    assert manager.get_setting("new_setting") == "value"

def test_persistence(clean_settings_file):
    # Test persistence by initializing a new SettingsManager instance
    manager = SettingsManager(filename="test_settings.json")
    manager.set_setting("show_dialog_on_start", False)
    del manager  # Delete the instance to ensure the file is written
    
    # Create a new SettingsManager instance and check the saved setting
    new_manager = SettingsManager(filename="test_settings.json")
    assert new_manager.get_setting("show_dialog_on_start") is False

def test_default_on_unknown_setting(clean_settings_file):
    # Test that an unknown setting returns the default value
    manager = SettingsManager(filename="test_settings.json")
    assert manager.get_setting("nonexistent_setting") is None
