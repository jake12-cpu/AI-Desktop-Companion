from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox
)
from PySide6.QtWidgets import QMessageBox
class SettingsWindow(QWidget):

    def __init__(self, config_manager=None):

        super().__init__()

        self.config_manager = config_manager

        self.setWindowTitle(
            "AI Companion 设置"
        )

        self.resize(
            350,
            250
        )


        self.init_ui()


    def init_ui(self):

        layout = QVBoxLayout()


        self.api_label = QLabel(
            "API Key"
        )

        self.api_input = QLineEdit()

        self.api_input.setEchoMode(
            QLineEdit.Password
        )

        self.provider_label = QLabel(
            "AI服务商"
        )

        self.provider_box = QComboBox()

        self.provider_box.addItems(
            [
                "DeepSeek",
                "OpenAI"
            ]
        )

        self.provider_box.currentTextChanged.connect(
            self.change_provider
        )
        self.model_label = QLabel(
            "模型"
        )


        self.model_box = QComboBox()

        self.model_box.addItems(
            [
                "deepseek-chat"
            ]
        )
        self.save_button = QPushButton(
            "保存"
        )


        self.save_button.clicked.connect(
            self.save
        )

        layout.addWidget(
            self.provider_label
        )

        layout.addWidget(
            self.provider_box
        )
        layout.addWidget(
            self.api_label
        )

        layout.addWidget(
            self.api_input
        )


        layout.addWidget(
            self.model_label
        )

        layout.addWidget(
            self.model_box
        )


        layout.addWidget(
            self.save_button
        )


        self.setLayout(
            layout
        )

    def change_provider(self, provider):

        self.model_box.clear()

        if provider == "DeepSeek":

            self.model_box.addItems(
                [
                    "deepseek-chat"
                ]
            )


        elif provider == "OpenAI":

            self.model_box.addItems(
                [
                    "gpt-4o",
                    "gpt-5"
                ]
            )
    def save(self):

        if self.config_manager:

            model = self.model_box.currentText()

            self.config_manager.set(
                "model",
                model
            )

            if model.startswith("gpt"):

                self.config_manager.set(
                    "base_url",
                    "https://api.openai.com/v1"
                )

            else:

                self.config_manager.set(
                    "base_url",
                    "https://api.deepseek.com"
                )

            self.config_manager.set(
                "api_key",
                self.api_input.text()
            )

            QMessageBox.information(
                self,
                "保存成功",
                f"当前模型：{model}"
            )