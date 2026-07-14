from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QInputDialog,
    QLineEdit
)
class MemoryPanel(QWidget):


    def __init__(
        self,
        memory_manager
    ):

        super().__init__()


        self.memory_manager = memory_manager


        self.setWindowTitle(
            "AI Companion 记忆管理"
        )


        self.resize(
            600,
            400
        )


        self.init_ui()


        self.load_memories()



    def init_ui(self):


        layout = QVBoxLayout()


        self.title = QLabel(
            "🧠 派蒙的长期记忆"
        )
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "搜索记忆..."
        )

        self.search_button = QPushButton(
            "搜索"
        )

        self.search_button.clicked.connect(
            self.search_memory
        )

        self.table = QTableWidget()
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setColumnCount(
            5
        )

        self.table.setHorizontalHeaderLabels(
            [
                "类型",
                "内容",
                "重要程度",
                "记忆强度",
                "使用次数"
            ]
        )



        self.refresh_button = QPushButton(
            "刷新"
        )
        self.delete_button = QPushButton(
            "删除选中记忆"
        )
        self.edit_button = QPushButton(
            "编辑选中记忆"
        )

        self.edit_button.clicked.connect(
            self.edit_selected_memory
        )

        self.delete_button.clicked.connect(
            self.delete_selected_memory
        )


        self.refresh_button.clicked.connect(
            self.load_memories
        )



        layout.addWidget(
            self.title
        )
        layout.addWidget(
            self.search_input
        )

        layout.addWidget(
            self.search_button
        )


        layout.addWidget(
            self.table
        )


        layout.addWidget(
            self.refresh_button
        )
        layout.addWidget(
            self.delete_button
        )
        layout.addWidget(
            self.edit_button
        )


        self.setLayout(
            layout
        )



    def load_memories(self):


        memories = self.memory_manager.get_memories()


        self.table.setRowCount(
            len(memories)
        )


        for row, memory in enumerate(memories):


            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    memory.get(
                        "type",
                        ""
                    )
                )
            )


            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    memory.get(
                        "content",
                        ""
                    )
                )
            )

            importance = memory.get(
                "importance",
                0
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        importance
                    )
                )
            )
            bar_length = int(
                importance * 10
            )

            bar = (
                    "█" * bar_length
                    +
                    "░" * (10 - bar_length)
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"{bar} {int(importance * 100)}%"
                )
            )


            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(
                        memory.get(
                            "used_count",
                            0
                        )
                    )
                )
            )

    def delete_selected_memory(self):

        row = self.table.currentRow()

        if row < 0:
            return

        content_item = self.table.item(
            row,
            1
        )

        if not content_item:
            return

        content = content_item.text()

        success = self.memory_manager.delete_memory(
            content
        )

        if success:
            self.load_memories()

    def edit_selected_memory(self):

        row = self.table.currentRow()

        if row < 0:
            return

        content_item = self.table.item(
            row,
            1
        )

        if not content_item:
            return

        old_content = content_item.text()

        new_content, ok = QInputDialog.getText(
            self,
            "编辑记忆",
            "修改内容:",
            text=old_content
        )

        if ok and new_content.strip():

            success = self.memory_manager.update_memory(
                old_content,
                new_content
            )

            if success:
                self.load_memories()

    def search_memory(self):

        keyword = self.search_input.text().strip()

        if keyword:

            memories = self.memory_manager.search_memory(
                keyword
            )

        else:

            memories = self.memory_manager.get_memories()

        self.table.setRowCount(
            len(memories)
        )

        for row, memory in enumerate(memories):
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    memory.get(
                        "type",
                        ""
                    )
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    memory.get(
                        "content",
                        ""
                    )
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        memory.get(
                            "importance",
                            0
                        )
                    )
                )
            )
            importance = memory.get(
                "importance",
                0
            )

            bar_length = int(
                importance * 10
            )

            bar = (
                    "█" * bar_length
                    +
                    "░" * (10 - bar_length)
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"{bar} {int(importance * 100)}%"
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(
                        memory.get(
                            "used_count",
                            0
                        )
                    )
                )
            )
