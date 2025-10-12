# hotkey_listener.py
import keyboard
from threading import Thread


class HotkeyListener:
    def __init__(self, timer_manager):
        self.timer_manager = timer_manager
        self.running = False

    def start(self):
        self.running = True
        thread = Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        while self.running:
            try:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key = event.name.upper()
                    self.timer_manager.input_key(key)
            except Exception as e:
                print(f"❌ 鍵盤監聽錯誤：{e}")