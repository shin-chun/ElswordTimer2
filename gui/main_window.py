from settings.common import *
from timer.manager import MainWindowManager
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

        # GridLayout for Button1–Button6
        grid_layout = QGridLayout()
        self.buttons = []
        buttons_labels = ['新增計時器', '編輯計時器', '儲存檔案', '刪除計時器', '重置計時器',
                          '匯入設定檔']
        for i in range(6):
            btn = QPushButton(buttons_labels[i])
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.buttons.append(btn)
            grid_layout.addWidget(btn, i // 3, i % 3)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setFont(font)

        self.manager = MainWindowManager(lambda: EditWindow(),
                                         event_list_widget=self.list_widget,
                                         window=self)

        # 按鈕功能綁定
        self.buttons[0].clicked.connect(self.handle_create_timer)
        self.buttons[1].clicked.connect(self.manager.edit_timer)
        self.buttons[2].clicked.connect(lambda: self.manager.save_file())
        self.buttons[3].clicked.connect(self.manager.delete_timer)
        self.buttons[4].clicked.connect(self.manager.reset_timer)
        self.buttons[5].clicked.connect(lambda: self.manager.import_config_via_dialog())

        self.list_widget.itemDoubleClicked.connect(lambda _: self.manager.edit_timer())

        # Bottom Button7
        self.bottom_button = QPushButton("啟動計時器")
        self.bottom_button.setFont(font)
        self.bottom_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bottom_button.clicked.connect(self.toggle_timer)

        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.addStretch()
        bottom_button_layout.addWidget(self.bottom_button)
        bottom_button_layout.addStretch()


        # Label
        self.label = QLabel("請點選按鈕")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.label)

        self.setLayout(main_layout)

    def handle_create_timer(self):
        name = self.manager.open_edit_window()
        print(f"使用者輸入：{name}")

    def toggle_timer(self):
        self.timer_running = not self.timer_running

        if self.timer_running:
            self.bottom_button.setText("停止計時器")
            self.label.setText("計時器已啟動")
            # TODO: 啟動計時邏輯
        else:
            self.bottom_button.setText("啟動計時器")
            self.label.setText("計時器已停止")
            # TODO: 停止計時邏輯

