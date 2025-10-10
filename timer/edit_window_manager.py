from gui import edit_window
from settings.common import *


class EditWindowManager:
    def __init__(self, key_labels, label_updater, event_list_widget, scan_code_store):
        self.key_labels = key_labels
        self.label_updater = label_updater
        self.event_list_widget = event_list_widget
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




