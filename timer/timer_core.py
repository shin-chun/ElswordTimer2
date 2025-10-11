from settings.common import *
from enum import Enum
from dataclasses import dataclass
from gui.cooldown_window import CooldownWindow, CooldownState


@dataclass
class Keys:
    first_key: str
    second_key: str
    third_key: str

@dataclass
class Keys2:
    first_key: str
    second_key: str
    third_key: str


class TimerState(Enum):
    IDLE = "空閒"
    SELECT = "選擇"
    LOCK = "鎖定"
    ACTIVE = "計時"


class TimerCore(QObject):
    def __init__(self, name, keys: Keys, keys2: Keys2, cooldown, callback=None):
        super().__init__()
        self.name = name
        self.keys = keys
        self.keys2 = keys2
        self.cooldown = cooldown
        self.callback = callback
        self.state = 'IDLE'
        self.remaining = cooldown
        # ✅ 明確初始化以下屬性
        self.active = False
        self.cooldown_window = None
        self.debug_mode = False  # 如果你要用 debug() 方法

    def update_config(self, keys: Keys, keys2: Keys2, cooldown: int):
        self.keys = keys
        self.keys2 = keys2
        self.cooldown = cooldown
        self.remaining = cooldown
        self.state = "IDLE"
        if hasattr(self, 'cooldown_window'):
            self.cooldown_window.update_duration(cooldown)
        print(f"🔄 TimerCore「{self.name}」已更新設定")

    def show_cooldown_window(self, state):
        print(f"✅ 顯示冷卻視窗：{self.name}")
        if self.cooldown_window is None:
            self.cooldown_window = CooldownWindow(self.name, self.cooldown)
        self.cooldown_window.set_state(state)
        self.cooldown_window.show()

    def stop_detection(self):
        # 停止鍵盤偵測或其他觸發邏輯
        self.active = False
        # 停止任何 thread 或 timer（如果有）

    def close_cooldown_window(self):
        if hasattr(self, 'cooldown_window') and self.cooldown_window.isVisible():
            self.cooldown_window.close()


    def check_key(self, key):
        if self.match_sequence(self.keys, key) or self.match_sequence(self.keys2, key):
            self.state = TimerState.ACTIVE
            self.start_countdown()

    def match_sequence(self, keys_obj, key):
        if keys_obj.third_key == key and not keys_obj.first_key and not keys_obj.second_key:
            return True

        if key == keys_obj.first_key:
            self.state = TimerState.SELECT
        elif self.state == TimerState.SELECT and key == keys_obj.second_key:
            self.state = TimerState.LOCK
        elif self.state == TimerState.LOCK and key == keys_obj.third_key:

            return True

        return False

    def start_countdown(self):
        print(f"🚀 觸發技能：{self.name}，倒數 {self.cooldown} 秒")
        self.remaining = self.cooldown
        # self.timer.start()
        self.state = TimerState.IDLE
        if self.callback:
            self.callback(self.name, self.remaining)

    def reset(self, cooldown=None):
        if cooldown is not None:
            self.cooldown = cooldown
        self.remaining = self.cooldown
        self.state = "IDLE"
        # 若有 timer 執行緒，這裡應該停止它
        if hasattr(self, 'cooldown_window'):
            self.cooldown_window.reset_display(self.cooldown)

    def start(self, state: CooldownState):
        if self.cooldown_window is None:
            self.cooldown_window = CooldownWindow(self.name, self.cooldown)
        self.cooldown_window.start(state)

    def debug(self, msg):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")


# app = QCoreApplication(sys.argv)
# keys_obj = TimerCore(
#     name='test_trigger',
#     keys=Keys('a', 'b', 'c'),
#     keys2=Keys2('d', 'e', 'f'),
#     cooldown=5
# )
#
# core_a = [ 'a', 'b', 'd', 'e', 'f', 'e', 'c']
# for k in core_a:
#     print(f'現在輸入：{k}')
#     time.sleep(0.5)
