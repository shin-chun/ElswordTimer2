from gui.edit_window import EditWindow
from gui.common import *
from timer.core import TimerCore

# EditWindow管理區



class EditWindowManager:
    def __init__(self, SCAN_CODE_MAP):
        self.recording_index = None
        self.key_labels = []
        self.SCAN_CODE_MAP = {
            29: "Left Ctrl",
            285: "Right Ctrl",
            42: "Left Shift",
            54: "Right Shift",
            56: "Left Alt",
            312: "Right Alt",
            # 可依需要補上更多鍵
        }


    def start_recording(self, index):
        self.recording_index = index
        self.key_labels[index].setText("等待按鍵...")

    def clear_key(self, index):
        self.key_labels[index].setText("None")
        if self.recording_index == index:
            self.recording_index = None

    def keyPressEvent(self, event):
        if self.recording_index is None:
            return

        scan_code = event.nativeScanCode()
        key_name = SCAN_CODE_MAP.get(scan_code)

        if not key_name:
            key_name = event.text().upper() or Qt.Key(event.key()).name.replace("Key_", "")

        self.key_labels[self.recording_index].setText(key_name)
        self.recording_index = None


class ButtonManager:
    def __init__(self):
        self.timers = []

    def create_edit_window(self):
        dialog = EditWindow(title='新增計時器')
        if dialog.exec():
            timer_name = dialog.name_input.text()
            print(f"新增的計時器名稱：{timer_name}")

    # def edit_timer(self, name, keys, cooldown, callback=None):
    #     timer = TimerCore(name=name, keys=keys, cooldown=cooldown, callback=callback)  # ✅ 關鍵
    #     print('pass')
    #
    # def save_file(self):
    #     print('pass')
    #
    # def delete_timer(self):
    #     print('pass')
    #
    # def reset_timer(self):
    #     print('pass')
    #
    # def import_config(self):
    #     print('pass')
    #
    # def input_key(self, key):
    #     print(f"🧩 TimerManager 收到鍵：{key}")
    #     for timer in self.timers:
    #         timer.input(key)


# class CooldownManager:
#     def update_countdown:
#
#     def update_label
