import sys

from PySide6.QtWidgets import QApplication

from ui.paimon_widget import PaimonWidget

app = QApplication(sys.argv)

window = PaimonWidget()

window.show()

sys.exit(app.exec())