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
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                print(f"🎹 鍵盤輸入：{key}")
                self.timer_manager.input_key(key)


class HotkeyController:
    def __init__(self, manager):
        self.manager = manager
        self.stage = 0
        self.selected = None

    def on_press(self, key):
        try:
            k = key.char.lower()
        except AttributeError:
            k = str(key).lower()

        if self.stage == 0:
            if k in self.manager.timers:
                self.selected = k
                self.stage = 1
                print(f"選擇：{k}")
        elif self.stage == 1:
            if k == 'shift':  # 第二鍵：鎖定
                self.stage = 2
                print(f"鎖定：{self.selected}")
        elif self.stage == 2:
            if k == 'enter':  # 第三鍵：觸發
                print(f"觸發：{self.selected}")
                self.manager.timers[self.selected].start()
                self.stage = 0  # 重置流程

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
