from settings.common import *
from timer.main_window_manager import MainWindowManager
from gui.edit_window import EditWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ElswordTimer")
        self.setGeometry(100, 100, 600, 450)
        self.timer_running = False  # 初始狀態：未啟動

        self.setStyleSheet("""
            QWidget { background-color: #f0f4f8; }
            QPushButton {
                background-color: #E0E0E0;
                color: black;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                min-width: 100px;
                min-height: 40px;
            }
            QPushButton:hover { background-color: #357ABD; }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                padding: 6px;
            }
        """)

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        # 初始化 UI 元件
        grid_layout = self.init_buttons(font)
        self.list_widget = self.init_list_widget(font)
        bottom_button_layout = self.init_bottom_button(font)
        self.label = self.init_label(font)

        # 建立 manager
        self.manager = MainWindowManager(lambda: EditWindow(),
                                         event_list_widget=self.list_widget,
                                         window=self)

        # 綁定按鈕功能
        self.bind_button_actions()

        # 主 layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.label)

        self.setLayout(main_layout)

    def init_buttons(self, font):
        grid_layout = QGridLayout()
        self.buttons = []
        buttons_labels = ['新增計時器', '編輯計時器', '儲存檔案', '刪除計時器', '重置計時器', '匯入設定檔']
        for i, label in enumerate(buttons_labels):
            btn = QPushButton(label)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.buttons.append(btn)
            grid_layout.addWidget(btn, i // 3, i % 3)
        return grid_layout

    def init_list_widget(self, font):
        list_widget = QListWidget()
        list_widget.setFont(font)
        return list_widget

    def init_bottom_button(self, font):
        self.bottom_button = QPushButton("啟動計時器")
        self.bottom_button.setFont(font)
        self.bottom_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bottom_button.clicked.connect(self.toggle_timer)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.bottom_button)
        layout.addStretch()
        return layout

    def init_label(self, font):
        label = QLabel("請點選按鈕")
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def bind_button_actions(self):
        actions = [
            self.handle_create_timer,
            self.manager.edit_timer,
            self.manager.save_file,
            self.manager.delete_timer,
            self.manager.reset_timer,
            self.manager.import_config_via_dialog
        ]
        for btn, action in zip(self.buttons, actions):
            btn.clicked.connect(action)

        self.list_widget.itemDoubleClicked.connect(lambda _: self.manager.edit_timer())

    def handle_create_timer(self):
        self.manager.open_edit_window()

    def toggle_timer(self):
        self.timer_running = not self.timer_running
        self.manager.toggle_timer(self.timer_running)
        self.update_ui_on_timer_toggle()

    def update_ui_on_timer_toggle(self):
        if self.timer_running:
            self.bottom_button.setText("停止計時器")
            self.label.setText("計時器已啟動")
        else:
            self.bottom_button.setText("啟動計時器")
            self.label.setText("計時器已停止")