import sys

from PySide6.QtWidgets import QApplication

from ui.paimon_widget import PaimonWidget
from core.ai_client import AIClient
from core.config_manager import ConfigManager

app = QApplication(sys.argv)

config_manager = ConfigManager()


client = AIClient(
    config_manager
)


window = PaimonWidget(
    client,
    config_manager
)
window.change_character("hutao")

window.show()

sys.exit(app.exec())
