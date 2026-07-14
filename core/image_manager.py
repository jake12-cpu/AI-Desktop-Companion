from pathlib import Path

from PySide6.QtGui import QPixmap


class ImageManager:

    def __init__(self):
        self.cache = {}


    def load_images(self, character_manager, state):

        character = character_manager.character_name

        cache_key = f"{character_manager.character_name}_{state}"

        if cache_key in self.cache:
            return self.cache[cache_key]


        folder = (
            Path(character_manager.get_character_path())
            / state
        )


        if not folder.exists():

            self.cache[cache_key] = []

            return []


        images = [

            QPixmap(str(file))

            for file in sorted(folder.iterdir())

            if file.suffix.lower() == ".png"

        ]


        self.cache[cache_key] = images

        return images