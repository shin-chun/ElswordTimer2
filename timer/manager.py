from settings.common import *
from settings.scan_code_resolver import *


class MainWindowManager:
    def __init__(self, create_window_factory):
        self.create_window_factory = create_window_factory

    def open_edit_window(self):
        dialog = self.create_window_factory()
        dialog.exec_()
        return dialog

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
    def __init__(self, key_labels, label_updater):
        self.key_labels = key_labels
        self.label_updater = label_updater
        self.recording_index = None

    def keyPressEvent(self, event):
        if self.recording_index is None:
            return
        scan_code = event.nativeScanCode()
        qt_key = event.key()

        if scan_code not in SCAN_CODE_MAP:
            key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
            SCAN_CODE_MAP[scan_code] = key_name
            save_scan_code_map(SCAN_CODE_MAP)
            print(f"📝 新增掃描碼：{scan_code} → {key_name}")
        else:
            key_name = SCAN_CODE_MAP[scan_code]
            print(f"🔁 已存在掃描碼：{scan_code} → {key_name}")

        if not key_name:
            key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
            SCAN_CODE_MAP[scan_code] = key_name
            save_scan_code_map(SCAN_CODE_MAP)
            print(f"📝 自動記錄：{scan_code} → {key_name}")

        self.key_labels[self.recording_index].setText(key_name)
        self.recording_index = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab and self.recording_index is not None:
                scan_code = event.nativeScanCode()
                key_name = SCAN_CODE_MAP.get(scan_code, "Tab")
                self.key_labels[self.recording_index].setText(key_name)
                self.recording_index = None
                return True  # 阻止 Qt 處理 TAB
        return super().eventFilter(obj, event)

    def clear_key(self, index):
        self.label_updater(index, "None")