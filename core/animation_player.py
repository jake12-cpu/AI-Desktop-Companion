from PySide6.QtCore import QObject, Signal, QTimer

from core.state import State


class AnimationPlayer(QObject):

    frame_changed = Signal(object)
    animation_finished = Signal()


    def __init__(self, image_manager, character_manager):

        super().__init__()

        self.image_manager = image_manager
        self.character_manager = character_manager

        self.current_state = State.IDLE

        self.images = []

        self.current_frame = 0

        self.animation_forward = True

        self.loop = True


        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.next_frame
        )


    def set_state(self, state, loop=True, interval=200):

        self.current_state = state

        self.current_frame = 0

        self.animation_forward = True

        self.loop = loop


        self.images = self.image_manager.load_images(
            self.character_manager,
            self.current_state.value
        )


        if self.images:

            self.frame_changed.emit(
                self.images[0]
            )


        self.timer.start(interval)



    def next_frame(self):

        if not self.images:
            return


        self.current_frame += 1


        if self.current_frame >= len(self.images):

            if self.loop:

                self.current_frame = 0

            else:

                self.current_frame = len(self.images) - 1

                self.timer.stop()

                self.animation_finished.emit()

                return


        self.frame_changed.emit(
            self.images[self.current_frame]
        )


    def change_character(self, character_manager):

        self.character_manager = character_manager

        self.images = []

        self.current_frame = 0

        self.set_state(
            State.IDLE,
            loop=True,
            interval=500
        )

    def stop(self):

        self.timer.stop()



    def current_pixmap(self):

        if not self.images:
            return None


        return self.images[
            self.current_frame
        ]