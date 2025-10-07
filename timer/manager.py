from settings.common import *
from settings.scan_code_resolver import *


class MainWindowManager:
    def __init__(self, create_window_factory):
        self.create_window_factory = create_window_factory

    def open_edit_window(self):
        dialog = self.create_window_factory()
        # if dialog.exec_() == QDialog.DialogCode.Accepted:
        #     data = dialog.get_data()
        #     name = data.get("name")
        #     keys = ','.join(data.get("keys"))
        #     item_text = f'{name} → {keys}'
        #     self.event_list_widget.addItem(item_text)


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


class EditWindowManager:
    def __init__(self, key_labels, label_updater, scan_code_store):
        self.key_labels = key_labels
        self.label_updater = label_updater
        self.scan_code_store = scan_code_store
        self.recording_index = None

    def start_recording(self, index):
        if self.recording_index is not None:
            print(f"⚠️ 正在錄製 index={self.recording_index}，忽略新的請求 index={index}")
            return
        self.recording_index = index
        print(f'🎬 開始錄製鍵位 index={index}')

    def keyPressEvent(self, event):
        """由主視窗的 eventFilter 傳入鍵盤事件"""
        if self.recording_index is None:
            return

        scan_code = event.nativeScanCode()
        qt_key = event.key()
        key_name = self.scan_code_resolver(scan_code, qt_key)

        self.label_updater(self.recording_index, key_name)
        self.recording_index = None

    def scan_code_resolver(self, scan_code: int, qt_key: int) -> str:
        if self.recording_index is None:
            return
        key_name = self.scan_code_store.get(scan_code)
        if not key_name:
            key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
            self.scan_code_store.set(scan_code, key_name)
            print(f"📝 新增掃描碼：{scan_code} → {key_name}")
        else:
            print(f"🔁 已存在掃描碼：{scan_code} → {key_name}")
        return key_name

    def handle_special_key(self, event) -> bool:
        special_keys = {
            Qt.Key.Key_Tab: "Tab",
            Qt.Key.Key_Escape: "Esc",
            Qt.Key.Key_Return: "Enter"
        }
        if self.recording_index is None:
            return False

        if event.key() in special_keys:
            scan_code = event.nativeScanCode()
            key_name = self.scan_code_store.get(scan_code) or special_keys[event.key()]
            self.label_updater(self.recording_index, key_name)
            self.recording_index = None
            print(event.key())
            return True
        return False

    def clear_key(self, index):
        self.label_updater(index, "None")
