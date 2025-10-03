from timer.core import Timer

class TimerManager:
    def __init__(self, callback=None):
        self.timers = []
        self.callback = callback

    def add_timer(self, name, keys, duration, window):
        sequence = {"keys": keys, "duration": duration, "window": window}
        timer = Timer(name=name, sequences=[sequence], callback=self.callback)  # ✅ 關鍵
        self.timers.append(timer)

    def input_key(self, key):
        print(f"🧩 TimerManager 收到鍵：{key}")
        for timer in self.timers:
            timer.input(key)