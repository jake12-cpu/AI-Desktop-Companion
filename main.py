import sys

from PySide6.QtWidgets import QApplication

from ui.paimon_widget import PaimonWidget
from core.ai_client import AIClient


app = QApplication(sys.argv)

client = AIClient()

window = PaimonWidget(client)

window.show()

sys.exit(app.exec())
