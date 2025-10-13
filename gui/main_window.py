from settings.common import *
from manager.main_window_manager import MainWindowManager
from manager.cooldown_manager import CooldownManager
from gui.cooldown_window import CooldownWindow
from gui.edit_window import EditWindow
from listen_hotkey.hotkey_listener import HotkeyListener
from timer.timer_factory import TimerFactory
from timer.timer_core import Keys, Keys2
from manager.group_state_manager import GroupStateManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ 建立群組管理器（只需要一次）
        self.group_manager = GroupStateManager()

        # ✅ 初始化技能容器
        self.timers = {}
        self.timer_cores = []

        # ✅ 初始化 UI 視窗
        self.setWindowTitle("ElswordTimer")
        self.setGeometry(100, 100, 600, 450)
        self.timer_running = False

        # ✅ 初始化樣式
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

        # ✅ 初始化 UI 元件
        grid_layout = self.init_buttons(font)
        self.list_widget = self.init_list_widget(font)
        bottom_button_layout = self.init_bottom_button(font)
        self.label = self.init_label(font)

        # ✅ 建立 TimerFactory（如果它不需要 cooldown_manager）
        self.timer_factory = TimerFactory()  # 或改寫成不依賴 cooldown_manager

        # ✅ 建立技能 TimerCore 並綁定管理器（每個技能會建立自己的 cooldown_window/manager）
        self.init_timers()

        # ✅ 建立主邏輯管理器
        self.manager = MainWindowManager(
            create_window_factory=lambda parent=None: EditWindow(parent=parent),
            event_list_widget=self.list_widget,
            window=self,
            cooldown_manager=None  # 如果你不再共用 cooldown_manager，可傳 None 或移除此參數
        )

        # ✅ 綁定按鈕功能
        self.bind_button_actions()

        # ✅ 主 layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.label)
        self.setLayout(main_layout)

        # ✅ 啟動熱鍵監聽
        self.hotkey_listener = HotkeyListener(self.manager)
        self.hotkey_listener.start()

        # ✅ 印出已建立技能
        print(f"📦 self.timers 包含技能：{list(self.timers.keys())}")

    def init_timers(self):
        configs = [
            {
                "name": "火球術",
                "keys": Keys("A", "S", "D"),
                "keys2": Keys2("Z", "X", "C"),
                "cooldown": 10
            },
            {
                "name": "冰凍術",
                "keys": Keys("Q", "W", "E"),
                "keys2": Keys2("U", "I", "O"),
                "cooldown": 15
            }
        ]

        self.timer_cores = []
        self.timers = {}

        for cfg in configs:
            # ✅ 建立冷卻視窗與管理器（每個技能獨立）
            cooldown_window = CooldownWindow(cfg["name"], cfg["cooldown"])
            cooldown_manager = CooldownManager(cooldown_window)

            # ✅ 建立 TimerCore
            timer = self.timer_factory.create(
                name=cfg["name"],
                keys=cfg["keys"],
                keys2=cfg["keys2"],
                cooldown=cfg["cooldown"],
                callback=self.on_timer_triggered
            )

            # ✅ 綁定群組（使用第一鍵作為群組名稱）
            group_name = cfg["keys"].first_key or "none"
            timer.bind_group(group_name)

            # ✅ 一次性綁定所有管理器與狀態
            timer.bind_managers(
                group_manager=self.group_manager,
                cooldown_manager=cooldown_manager,
                debug=True,
                enabled=True
            )

            # ✅ 加入管理列表
            self.timers[cfg["name"]] = timer
            self.timer_cores.append(timer)

        # ✅ 所有 TimerCore 建立完後，統一綁定 all_timers
        for timer in self.timer_cores:
            timer.bind_all_timers(self.timer_cores)

        print(f"🧩 已建立 TimerCore：{list(self.timers.keys())}")

    def on_timer_triggered(self, name, remaining):
        print(f"✅ 技能「{name}」觸發，剩餘 {remaining} 秒")

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
            self.manager.delete_timer_by_name_from_selection,  # ✅ 修正這行,
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

    def closeEvent(self, event):
        self.cooldown_manager.close_all_windows()
        # self.save_config_on_exit()
        event.accept()

    def save_config_on_exit(self):
        self.manager.save_file_to_path("event_data.json")



