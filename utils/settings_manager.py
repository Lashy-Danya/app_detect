import json
from pathlib import Path
from typing import Any, Dict, Union

# TODO: PEP 257
class SettingsManager:
    """
    A class to manage application settings.

    Attributes:
        DEFAULT_SETTINGS (Dict[str, Any]): Default settings for the application.
        filename (Path): The filename/path to the settings file.
        settings (Dict[str, Any]): Current settings loaded from the settings file.
    """

    # Define default settings as a class attribute
    DEFAULT_SETTINGS: Dict[str, Any] = {
        # Add more default settings here
    }

    def __init__(self, filename: Union[str, Path] = "settings.json") -> None:
        """
        Initializes the SettingsManager with the specified filename.

        Args:
            filename (Union[str, Path], optional): The filename/path to the settings file. 
                Defaults to "settings.json".
        """
        self.filename = Path(filename)
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """
        Loads settings from the settings file.

        Returns:
            Dict[str, Any]: The loaded settings.
        """
        if not self.filename.exists():
            return self.DEFAULT_SETTINGS.copy()
        
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_SETTINGS.copy()
        
    def save_settings(self) -> None:
        """
        Saves current settings tot the settings file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)
        
    def get_setting(self, key: str) -> Any:
        """
        Retrieves the value of a specific setting.

        Args:
            key (str): The key of the setting.

        Returns:
            Any: The value of the setting.
        """
        return self.settings.get(key, self.DEFAULT_SETTINGS.get(key))
    
    def set_setting(self, key: str, value: Any) -> None:
        """
        Sets the value of a specific setting.

        Args:
            key (str): The key of the setting.
            value (Any): The value to set.
        """
        self.settings[key] = value
        self.save_settings()

    def update_settings(self, new_settings: Dict[str, Any]) -> None:
        """
        Updates multiple settings with the provided dictionary.

        Args:
            new_settings (Dict[str, Any]): A dictionary containing settings to update.
        """
        self.settings.update(new_settings)
        self.save_settings()