import json

from pathlib import Path


class SettingsManager:
    def __init__(self, filename="settings.json") -> None:
        self.filename = Path(filename)

        self.default_settings = {
            "show_dialog_on_start": True
        }

        self.settings = self.load_settings()

    def load_settings(self):
        if self.filename.exists():
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()
        
    def get_setting(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set_setting(self, key, value):
        self.settings[key] = value
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)