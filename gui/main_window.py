from PySide6.QtWidgets import (
    QWidget, QPushButton, QListWidget, QLabel,
    QVBoxLayout, QGridLayout, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分離式 UI")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("""
            QWidget { background-color: #f0f4f8; }
            QPushButton {
                background-color: #4a90e2;
                color: white;
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

        # GridLayout for Button1–Button6
        grid_layout = QGridLayout()
        self.buttons = []
        for i in range(6):
            btn = QPushButton(f"Button{i+1}")
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.buttons.append(btn)
            grid_layout.addWidget(btn, i // 3, i % 3)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setFont(font)

        # Bottom Button7
        self.bottom_button = QPushButton("Button7")
        self.bottom_button.setFont(font)
        self.bottom_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.addStretch()
        bottom_button_layout.addWidget(self.bottom_button)
        bottom_button_layout.addStretch()

        # Label
        self.label = QLabel("請點選按鈕")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.label)

        self.setLayout(main_layout)