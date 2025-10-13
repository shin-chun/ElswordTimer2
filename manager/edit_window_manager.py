from settings.common import *
from threading import Thread



class EditWindowManager:
    def __init__(self, key_labels, label_updater, scan_code_store, event_data=None, keyboard_owner=None):
        self.key_labels = key_labels
        self.label_updater = label_updater
        self._event_data = event_data or {}
        self.scan_code_store = scan_code_store
        self.recording_index = None
        # self.keyboard_owner = keyboard_owner
        self.listener = None

    def start_recording(self, index):
        if self.recording_index is not None:
            print(f"⚠️ 正在錄製 index={self.recording_index}，忽略新的請求 index={index}")
            return
        self.recording_index = index
        self.listener = keyboard.Listener(on_press=self._on_key_event)
        Thread(target=self.listener.start, daemon=True).start()
        print(f"🎬 開始錄製 index={index}")

    def _on_key_event(self, key):
        if self.recording_index is None:
            return

        try:
            key_name = self.resolve_key_name(key)
            print(f"[錄製] index={self.recording_index}, key={key_name}")
            self.label_updater(self.recording_index, key_name)
            self.recording_index = None
            self.listener.stop()
            self.listener = None
        except Exception as e:
            print(f"❌ 錄製錯誤：{e}")

    def resolve_key_name(self, key):
        if isinstance(key, keyboard.Key):
            mapping = {
                keyboard.Key.ctrl_l: "Left Ctrl",
                keyboard.Key.ctrl_r: "Right Ctrl",
                keyboard.Key.shift_l: "Left Shift",
                keyboard.Key.shift_r: "Right Shift",
                keyboard.Key.alt_l: "Left Alt",
                keyboard.Key.alt_r: "Right Alt",
                keyboard.Key.enter: "Enter",
                keyboard.Key.space: "Space",
                keyboard.Key.esc: "Esc",
                keyboard.Key.tab: "Tab",
                keyboard.Key.backspace: "Backspace",
                keyboard.Key.up: "Up Arrow",
                keyboard.Key.down: "Down Arrow",
                keyboard.Key.left: "Left Arrow",
                keyboard.Key.right: "Right Arrow",
            }
            return mapping.get(key, key.name)
        else:
            return str(key).replace("'", "")

    def clear_key(self, index):
        self.label_updater(index, "None")

    def load_event_data(self):
        return self._event_data

    def store_event_data(self, data):
        self._event_data = data

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





