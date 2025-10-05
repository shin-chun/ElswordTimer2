from gui.common import *


manager = EditWindowManager()


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', manager=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.manager = EditWindowManager(self)
        self.setMinimumSize(600, 200)  # 調整視窗大小以容納 6x4 格線

        self.recording_index = None
        self.key_labels = []

        layout = QVBoxLayout()
        grid = QGridLayout()
        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '選擇鍵2', '鎖定鍵2', '觸發鍵2']

        for i in range(6):
            col = i % 3 * 2  # 每組佔 2 欄（按鈕 + label/清除）
            row_base = i // 3 * 2  # 每組佔 2 行

            # 錄製按鈕：佔 2 行 × 1 欄
            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(record_btn, row_base, col, 2, 1)

            # 顯示 Label：佔 1 行 × 1 欄
            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(label, row_base, col + 1)

            # 清除按鈕：佔 1 行 × 1 欄（在 label 下方）
            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(clear_btn, row_base + 1, col + 1)

            record_btn.clicked.connect(lambda _, idx=i: self.manager.start_recording(idx))
            clear_btn.clicked.connect(lambda _, idx=i: self.manager.clear_key(idx))

            self.key_labels.append(label)

        layout.addLayout(grid)
        self.setLayout(layout)
