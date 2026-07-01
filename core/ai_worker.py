from PySide6.QtCore import QThread, Signal


class AIWorker(QThread):

    finished = Signal(str)

    def __init__(self, client, message):
        super().__init__()

        self.client = client
        self.message = message

    def run(self):
        reply = self.client.chat(self.message)

        self.finished.emit(reply)