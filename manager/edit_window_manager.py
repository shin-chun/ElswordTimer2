from gui import edit_window
from settings.common import *


class EditWindowManager:
    def __init__(self, key_labels, label_updater, scan_code_store, event_data=None, keyboard_owner=None):
        self.key_labels = key_labels
        self.label_updater = label_updater
        self._event_data = event_data or {}
        self.scan_code_store = scan_code_store
        self.recording_index = None
        self.keyboard_owner = keyboard_owner


    def start_recording(self, index):
        if self.recording_index is not None:
            print(f"⚠️ 正在錄製 index={self.recording_index}，忽略新的請求 index={index}")
            return
        self.recording_index = index
        self.keyboard_owner.grabKeyboard()
        print(f'🎬 開始錄製鍵位 index={index}')

    def keyPressEvent(self, event):
        """由主視窗的 eventFilter 傳入鍵盤事件"""
        if self.recording_index is None:
            return

        # ① 取得鍵盤資訊
        scan_code = event.nativeScanCode()
        qt_key = event.key()

        # ② 解析鍵名（方向鍵、功能鍵等）
        key_name = self.scan_code_resolver(scan_code, qt_key)

        # ③ 除錯用：可選擇性印出鍵名
        print(f"[錄製] index={self.recording_index}, key={key_name}")

        # ④ 更新 UI 顯示
        self.label_updater(self.recording_index, key_name)

        # ⑤ 結束錄製狀態
        self.recording_index = None
        self.keyboard_owner.releaseKeyboard()
        # ⑥ 阻止事件繼續傳遞（可選）
        event.accept()

    def scan_code_resolver(self, scan_code: int, qt_key: int) -> str:
        key_map = {
            Qt.Key.Key_Left: "LEFT",
            Qt.Key.Key_Right: "RIGHT",
            Qt.Key.Key_Up: "UP",
            Qt.Key.Key_Down: "DOWN",
            Qt.Key.Key_Escape: "ESC",
            Qt.Key.Key_Return: "ENTER",
            Qt.Key.Key_Space: "SPACE",
            # 可擴充更多鍵
        }

        # 若有對應鍵名，直接回傳
        if qt_key in key_map:
            return key_map[qt_key]

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

    # def store_event_data(self, data: dict):
    #     """儲存事件資料到 JSON 檔案"""
    #     try:
    #         with open(self.storage_path, "w", encoding="utf-8") as f:
    #             json.dump(data, f, ensure_ascii=False, indent=2)
    #     except Exception as e:
    #         print(f"[儲存失敗] {e}")
    #
    # def load_event_data(self) -> dict:
    #     """載入事件資料（若存在）"""
    #     if not os.path.exists(self.storage_path):
    #         return {}
    #     try:
    #         with open(self.storage_path, "r", encoding="utf-8") as f:
    #             return json.load(f)
    #     except Exception as e:
    #         print(f"[載入失敗] {e}")
    #         return {}

    def load_event_data(self):
        return self._event_data

    def store_event_data(self, data):
        self._event_data = data





