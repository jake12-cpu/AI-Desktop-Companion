from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from core.character_manager import CharacterManager

class CharacterMenu(QMenu):

    def __init__(self, parent=None):

        super().__init__("切换角色", parent)


        self.characters = CharacterManager.get_all_characters()


        self.actions = {}


        for character in self.characters:

            action = QAction(
                character,
                self
            )

            self.addAction(action)

            self.actions[character] = action
            self.settings_action = QAction(
                "设置",
                self
            )

            self.addSeparator()

            self.addAction(
                self.settings_action
            )