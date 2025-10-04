import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    # 綁定按鈕事件
    # for i, btn in enumerate(window.buttons):
    #     btn.clicked.connect(lambda _, x=i+1: handle_click(window, x))
    # window.bottom_button.clicked.connect(lambda: handle_click(window, 7))

    window.show()
    sys.exit(app.exec())


def handle_click(ui, index):
    text = f"你按了 Button{index}"
    ui.label.setText(text)
    ui.list_widget.addItem(text)


if __name__ == "__main__":
    main()
