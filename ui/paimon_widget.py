import random
import os

from PySide6.QtCore import QPoint, QPropertyAnimation, QTimer, Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel, QLineEdit, QWidget

from core.ai_worker import AIWorker
from core.image_manager import ImageManager
from core.message_manager import MessageManager
from core.memory_manager import MemoryManager
from core.state import State
from core.animation_player import AnimationPlayer
from core.bubble_manager import BubbleManager
from core.character_manager import CharacterManager
from core.character_menu import CharacterMenu
from ui.settings_window import SettingsWindow
from core.memory_extractor import MemoryExtractor

class PaimonWidget(QWidget):
    FRAME_INTERVAL_MS = 150
    BREATHE_INTERVAL_MS = 16
    TYPING_INTERVAL_MS = 45
    INACTIVITY_TIMEOUT_MS = 8000
    BUBBLE_HIDE_MS = 3000
    BLINK_INTERVAL_RANGE_MS = (5000, 10000)
    IDLE_MESSAGE_RANGE_MS = (30000, 90000)

    LOOP_STATES = {State.IDLE, State.SLEEP}

    def __init__(
            self,
            client,
            config_manager
    ):
        super().__init__()
        self.client = client
        self.config_manager = config_manager
        self.character = "paimon"
        self.character_manager = CharacterManager(
            self.character
        )

        self.character = (
            self.character_manager.character_name
        )

        self._init_runtime_state()
        self._init_managers()
        self._init_window()
        self._init_widgets()
        self._init_animations()
        self._init_timers()
        self._init_menu()

        self.animation_player.set_state(
            State.IDLE,
            loop=True,
            interval=500
        )
    # ---------- init sections ----------
    def _init_runtime_state(self):
        self.base_x = 100
        self.base_y = 100
        self.image_top = 60
        self.breathe_offset = 0
        self.breathe_direction = 1
        self.drag_position = None
        self.is_dragging = False
        self.worker = None
        self.settings_window = None

    def _init_character(self):

        from core.character_manager import CharacterManager

        self.character_manager = CharacterManager(
            self.character
        )

    def _init_managers(self):

        self.image_manager = ImageManager()

        self.character_manager = CharacterManager(
            self.character
        )

        self.animation_player = AnimationPlayer(
            self.image_manager,
            self.character_manager
        )

        self.animation_player.frame_changed.connect(
            self.update_character_image
        )

        self.animation_player.animation_finished.connect(
            self.on_animation_finished
        )

        self.message_manager = MessageManager(
            self.character_manager
        )

        self.memory_extractor = MemoryExtractor()

        self.memory_manager = MemoryManager()
    def update_character_image(self, pixmap):

        if pixmap:
            self.image_label.setPixmap(
                pixmap
            )

    def update_input_placeholder(self):

        names = {
            "paimon": "派蒙",
            "hutao": "胡桃"
        }

        name = names.get(
            self.character,
            self.character
        )

        self.input_box.setPlaceholderText(
            f"和{name}聊聊天吧..."
        )

    def on_animation_finished(self):

        self.animation_player.set_state(
            State.IDLE,
            loop=True,
            interval=500
        )
    def _init_window(self):
        fallback_pixmap = QPixmap(
            os.path.join(
                self.character_manager.get_character_path(),
                "paimon.png"
            )
        )
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(
            fallback_pixmap.width(),
            fallback_pixmap.height() + self.image_top,
        )
        self.move(self.base_x, self.base_y)

    def _init_widgets(self):
        fallback_pixmap = QPixmap(
            os.path.join(
                self.character_manager.get_character_path(),
                "paimon.png"
            )
        )
        self.image_label = QLabel(self)
        self.image_label.setPixmap(fallback_pixmap)
        self.image_label.move(0, self.image_top)

        self.message_label = QLabel("你好，旅行者！", self)
        self.message_label.setWordWrap(True)
        self.message_label.setMaximumWidth(260)
        self.message_label.setStyleSheet(
            """
            QLabel {
                background-color: white;
                color: black;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #dddddd;
            }
            """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.message_label.setGraphicsEffect(shadow)
        self.message_label.move(20, 20)
        self.message_label.hide()
        self.bubble_manager = BubbleManager(
            self.message_label
        )

        self.bubble_manager.apply_style()

        self.input_box = QLineEdit(self)

        self.update_input_placeholder()
        self.input_box.move(
            20,
            self.height() - 60
        )
        self.input_box.resize(220, 28)
        self.input_box.returnPressed.connect(self.show_message)
        self.input_box.hide()

    def _init_animations(self):
        self.bubble_animation = QPropertyAnimation(self.message_label, b"pos")

    def _init_timers(self):
        self.breathe_timer = QTimer(self)
        self.breathe_timer.timeout.connect(self.breathe)
        self.breathe_timer.start(self.BREATHE_INTERVAL_MS)
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.random_blink)
        self.schedule_blink()
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.setSingleShot(True)
        self.inactivity_timer.timeout.connect(self.to_idle)
        self.restart_inactivity_timer()

        self.idle_message_timer = QTimer(self)
        self.idle_message_timer.setSingleShot(True)
        self.idle_message_timer.timeout.connect(self.show_idle_message)
        self.schedule_idle_message()

    # ---------- input / mouse ----------
    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.RightButton:
            self.character_menu.exec(
                event.globalPosition().toPoint()
            )

            return

        if event.button() != Qt.MouseButton.LeftButton:
            return
        self.restart_inactivity_timer()

        self.drag_position = (
            event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        )
        self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.drag_position is None:
            return

        self.is_dragging = True
        new_pos = event.globalPosition().toPoint() - self.drag_position
        self.base_x = new_pos.x()
        self.base_y = new_pos.y()
        self.move(self.base_x, self.base_y)

    def mouseReleaseEvent(self, event):
        self.drag_position = None

        if not self.is_dragging:
            self.input_box.show()
            self.input_box.setFocus()
            self.input_box.selectAll()

    def show_message(self):
        text = self.input_box.text().strip()
        if not text:
            self.restart_inactivity_timer()
            return

        self.restart_inactivity_timer()
        self.idle_message_timer.stop()

        self.message_manager.add_user_message(text)

        memories = self.memory_extractor.extract(text)

        for memory in memories:
            self.memory_manager.add_memory(
                memory
            )

        self.message_label.setText("派蒙思考中...")
        self.message_label.adjustSize()
        self.message_label.show()
        self.animation_player.set_state(
            State.THINKING,
            loop=True,
            interval=300
        )

        self.input_box.setEnabled(False)
        self.input_box.clear()
        self.input_box.hide()

        messages = self.message_manager.get_messages()

        memory_context = self.message_manager.get_memory_context(
            self.memory_manager.get_memories()
        )

        if memory_context:
            messages.insert(
                1,
                memory_context
            )

        messages = self.message_manager.get_messages()

        memory_prompt = self.memory_manager.build_memory_prompt()

        if memory_prompt:
            messages.insert(
                1,
                {
                    "role": "system",
                    "content": memory_prompt
                }
            )

        self.worker = AIWorker(
            self.client,
            messages
        )

        self.worker.finished.connect(
            self.show_ai_reply
        )

        self.worker.start()
    # ---------- AI / bubble ----------
    def show_ai_reply(self, reply):
        if not reply:
            reply = "旅行者，我刚刚好像走神了！"

        self.input_box.setEnabled(True)

        self.input_box.move(
            20,
            self.height() - 60
        )

        self.input_box.show()
        self.input_box.raise_()
        self.message_manager.add_assistant_message(reply)
        self.bubble_manager.type_text(reply)
        self.bubble_manager.play_enter_animation()
        self.animation_player.set_state(
            State.TALK,
            loop=True,
            interval=150
        )
        self.restart_inactivity_timer()
        self.schedule_idle_message()
    # ---------- state / timers ----------
    def _set_state_if_current(self, expected_state, next_state):

        if self.animation_player.current_state == expected_state:
            self.animation_player.set_state(
                next_state,
                loop=True,
                interval=500
            )
    def to_idle(self):
        if self.animation_player.current_state not in (
                State.THINKING,
                State.TALK
        ):
            self.animation_player.set_state(
                State.IDLE,
                loop=True,
                interval=500
            )

    def restart_inactivity_timer(self):
        self.inactivity_timer.start(self.INACTIVITY_TIMEOUT_MS)

    def schedule_blink(self):
        self.blink_timer.start(random.randint(*self.BLINK_INTERVAL_RANGE_MS))

    def random_blink(self):
        if self.animation_player.current_state == State.IDLE:
            self.animation_player.set_state(
                State.BLINK,
                loop=False,
                interval=120
            )
        self.schedule_blink()

    def schedule_idle_message(self):
        self.idle_message_timer.start(random.randint(*self.IDLE_MESSAGE_RANGE_MS))

    def show_idle_message(self):
        if self.animation_player.current_state != State.IDLE:
            self.schedule_idle_message()
            return

        text = self.message_manager.get_random_idle_message()
        self.message_label.setText(text)
        self.message_label.adjustSize()
        self.message_label.show()

        QTimer.singleShot(self.BUBBLE_HIDE_MS, self.message_label.hide)
        self.schedule_idle_message()

    # ---------- character animation ----------
    def breathe(self):
        self.breathe_offset += self.breathe_direction

        if self.breathe_offset >= 10:
            self.breathe_direction = -1
        elif self.breathe_offset <= 0:
            self.breathe_direction = 1

        self.image_label.move(0, self.image_top + self.breathe_offset)

    def _current_images(self):
        if self.animation_player.current_state is None:
            return []

        return self.image_manager.load_images(
            self.character,
            self.animation_player.current_state.value
        )
    def change_character(self, name):

        self.character_manager.change_character(
            name
        )

        self.character = name


        self.animation_player.change_character(
            self.character_manager
        )
        self.update_input_placeholder()

        self.message_manager = MessageManager(
            self.character_manager
        )

    def _init_menu(self):

        self.character_menu = CharacterMenu(
            self
        )
        self.character_menu.settings_action.triggered.connect(
            self.open_settings
        )

        for name, action in self.character_menu.actions.items():
            action.triggered.connect(
                lambda checked=False, n=name:
                self.change_character(n)
            )

    def open_settings(self):

        if self.settings_window is None:
            self.settings_window = SettingsWindow(
                self.config_manager
            )

        self.settings_window.show()

