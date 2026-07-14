from PySide6.QtCore import QTimer, QPoint, QPropertyAnimation
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect


class BubbleManager:

    def __init__(self, label):

        self.label = label

        self.full_text = ""
        self.current_index = 0

        self.typing_interval = 45
        self.hide_delay = 3000


        self.type_timer = QTimer()
        self.type_timer.timeout.connect(
            self.type_next_character
        )


    def show(self, text):

        self.label.setText(text)
        self.label.adjustSize()
        self.label.show()


    def type_text(self, text):

        self.full_text = text
        self.current_index = 0

        self.label.setText("")

        self.label.show()

        self.type_timer.start(
            self.typing_interval
        )


    def type_next_character(self):

        if self.current_index >= len(self.full_text):

            self.type_timer.stop()

            QTimer.singleShot(
                self.hide_delay,
                self.hide
            )

            return


        self.current_index += 1

        self.label.setText(
            self.full_text[:self.current_index]
        )

        self.label.adjustSize()



    def hide(self):

        self.label.hide()


    def play_enter_animation(self):

        animation = QPropertyAnimation(
            self.label,
            b"pos"
        )

        animation.setDuration(200)

        animation.setStartValue(
            self.label.pos() - QPoint(0,10)
        )

        animation.setEndValue(
            self.label.pos()
        )

        animation.start()



    def apply_style(self):

        self.label.setStyleSheet(
            """
            QLabel {
                background-color:white;
                color:black;
                border-radius:12px;
                padding:10px;
                font-size:14px;
                border:1px solid #dddddd;
            }
            """
        )

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(40)
        shadow.setOffset(5,5)
        shadow.setColor(
            QColor(0,0,0,180)
        )

        self.label.setGraphicsEffect(shadow)