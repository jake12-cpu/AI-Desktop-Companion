from PySide6.QtCore import QThread, Signal


class AIWorker(QThread):

    finished = Signal(str)

    def __init__(self, client, messages):
        super().__init__()

        self.client = client
        self.messages = messages

    def run(self):

        try:

            reply = self.client.chat(
                self.messages
            )

            self.finished.emit(reply)


        except Exception as e:

            self.finished.emit(
                "派蒙暂时连接不上服务器了..."
            )

            print(
                "AI错误:",
                e
            )
