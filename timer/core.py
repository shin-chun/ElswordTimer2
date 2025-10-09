import time
from settings.common import *
from enum import Enum
from dataclasses import dataclass
import sys


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
        self.state = TimerState.IDLE
        self.remaining = 0

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

    def reset(self):
        self.state = TimerState.IDLE
        self.remaining = 0
        self.timer.stop()

    def debug(self, msg):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")

app = QCoreApplication(sys.argv)
keys_obj = TimerCore(
    name='test_trigger',
    keys=Keys('a', 'b', 'c'),
    keys2=Keys2('d', 'e', 'f'),
    cooldown=5
)

core_a = [ 'a', 'b', 'd', 'e', 'f', 'e', 'c']
for k in core_a:
    print(f'現在輸入：{k}')
    time.sleep(0.5)
