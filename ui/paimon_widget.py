import random

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt,QTimer
from PySide6.QtCore import (
    Qt,
    QPoint,
    QTimer,
    QPropertyAnimation
)
from core.message_manager import MessageManager




class PaimonWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.offset = 0

        self.direction = 1

        self.timer = QTimer()

        self.timer.timeout.connect(self.breathe)

        self.timer.start(16)

        pixmap = QPixmap("assets/paimon.png")
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.image_top = 60

        self.resize(
            pixmap.width(),
            pixmap.height() + self.image_top
        )
        self.image_label.move(
            0,
            self.image_top
        )
        self.base_x = 100
        self.base_y = 100

        self.move(self.base_x, self.base_y)
        self.drag_position = None
        self.message_label = QLabel("你好，旅行者！", self)
        self.message_label.hide()
        self.message_manager = MessageManager()
        self.is_dragging = False

        self.messages = [
            "你好，旅行者！",
            "今天学习了吗？",
            "加油，我陪着你！",
            "要不要休息一下？",
            "嘿嘿~",
            "又在写代码呀？"
        ]

        self.message_label.setStyleSheet("""
        background:white;
        border-radius:8px;
        padding:5px;
        font-size:14px;
        """)

        self.message_label.adjustSize()

        self.message_label.move(20, 20)
        self.bubble_animation = QPropertyAnimation(
            self.message_label,
            b"pos"
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                    event.globalPosition().toPoint()
                    - self.frameGeometry().topLeft()
            )

            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.is_dragging = True
            new_pos = event.globalPosition().toPoint() - self.drag_position

            self.base_x = new_pos.x()
            self.base_y = new_pos.y()

            self.move(
                self.base_x,
                self.base_y
            )

    def mouseReleaseEvent(self, event):

        self.drag_position = None

        if not self.is_dragging:
            self.show_message()

    def breathe(self):

        self.offset += self.direction

        if self.offset >= 10:
            self.direction = -1

        elif self.offset <= 0:
            self.direction = 1

        self.image_label.move(
            0,
            self.image_top + self.offset
        )

    def show_message(self):
        text = self.message_manager.random_message()

        self.message_label.setText(text)
        self.message_label.adjustSize()

        self.message_label.show()
        self.bubble_animation.stop()

        self.bubble_animation.setDuration(200)

        self.bubble_animation.setStartValue(
            self.message_label.pos() - QPoint(0, 10)
        )

        self.bubble_animation.setEndValue(
            self.message_label.pos()
        )

        self.bubble_animation.start()

        QTimer.singleShot(3000, self.message_label.hide)