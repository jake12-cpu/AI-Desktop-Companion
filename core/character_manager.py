import json
import os


class CharacterManager:

    def __init__(self, character_name):

        self.character_name = character_name

        self.character_path = os.path.join(
            "characters",
            character_name
        )

        self.config = self.load_config()


    def load_config(self):

        config_path = os.path.join(
            self.character_path,
            f"{self.character_name}.json"
        )

        if not os.path.exists(config_path):
            return {}

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)


    def get_name(self):

        return self.config.get(
            "name",
            self.character_name
        )


    def get_system_prompt(self):

        return self.config.get(
            "system_prompt",
            ""
        )


    def get_character_path(self):

        return self.character_path
    def change_character(self, character_name):

        self.character_name = character_name

        self.character_path = os.path.join(
            "characters",
            character_name
        )

        self.config = self.load_config()
    @staticmethod
    def get_all_characters():

        characters = []

        root = "characters"

        if not os.path.exists(root):
            return characters


        for name in os.listdir(root):

            path = os.path.join(
                root,
                name
            )

            if os.path.isdir(path):

                json_path = os.path.join(
                    path,
                    f"{name}.json"
                )

                if os.path.exists(json_path):

                    characters.append(name)


        return characters