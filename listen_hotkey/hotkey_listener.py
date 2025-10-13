from pynput import keyboard
from threading import Thread

class HotkeyListener:
    def __init__(self, timer_manager):
        self.timer_manager = timer_manager
        self.listener = None
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            thread = Thread(target=self.listener.start, daemon=True)
            thread.start()

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
        if not self.running:
            return

        try:
            if isinstance(key, keyboard.Key):
                # 處理特殊鍵（例如左右 Ctrl）
                if key == keyboard.Key.ctrl_l:
                    key_name = "Left Ctrl"
                elif key == keyboard.Key.ctrl_r:
                    key_name = "Right Ctrl"
                elif key == keyboard.Key.shift_l:
                    key_name = "Left Shift"
                elif key == keyboard.Key.shift_r:
                    key_name = "Right Shift"
                elif key == keyboard.Key.alt_l:
                    key_name = "Left Alt"
                elif key == keyboard.Key.alt_r:
                    key_name = "Right Alt"
                else:
                    key_name = key.name.upper()
            else:
                # 處理一般字母或數字鍵
                key_name = str(key).replace("'", "").upper()

            print(f"🎹 鍵盤輸入：{key_name}")
            self.timer_manager.input_key(key_name)

        except Exception as e:
            print(f"❌ 鍵盤監聽錯誤：{e}")