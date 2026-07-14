import json
import os
from PySide6.QtCore import QObject, Signal

class ConfigManager(QObject):
    config_changed = Signal(str, object)
    def __init__(self):

        super().__init__()

        self.path = "config/config.json"

        self.config = {}

        self.load()


    def load(self):

        if not os.path.exists(self.path):

            self.config = {
                "api_key": "",
                "base_url": "https://api.deepseek.com",
                "model": "deepseek-chat"
            }

            self.save()

        else:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                self.config = json.load(f)



    def save(self):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.config,
                f,
                indent=4,
                ensure_ascii=False
            )



    def get(self, key):

        return self.config.get(
            key,
            ""
        )

    def set(self, key, value):

        self.config[key] = value

        self.save()

        self.config_changed.emit(
            key,
            value
        )