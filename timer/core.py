import time
from enum import Enum, auto
from dataclasses import dataclass


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
    IDLE = "idle"
    SELECT = "select"
    LOCK = "locked"
    ACTIVE = "running"


class TimerCore:
    def __init__(self, name, keys: Keys, keys2: Keys2, cooldown, callback=None):
        self.debug_mode = None
        self.name = name
        self.keys = keys
        self.keys2 = keys2
        self.cooldown = cooldown
        self.callback = callback
        self.state = TimerState.IDLE
        self.last_times = [None]

    def check_key(self, key):
        now = time.time()
        if self.match_sequence(self.keys, key) or self.match_sequence(self.keys2, key):
            self.state = TimerState.ACTIVE
            self.trigger(self.cooldown)

        # print(seq['keys'], type(seq['keys']))

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

    def trigger(self, cooldown):
        print(f"🚀 觸發技能：{self.name}，倒數 {cooldown} 秒")
        if self.callback:
            self.callback(self.name, cooldown)

    def reset(self):
        self.state = TimerState.IDLE
        self.last_times[0] = None

    def debug(self, msg):
        self.debug_mode = False
        if self.debug_mode:
            print(f"[DEBUG] {msg}")


# trigger = TimerCore(
#     name='test_trigger',
#     keys=Keys('a','b', 'c'),
#     keys2=Keys2('a', 'b', 'd'),
#     # second_keys=[['a', 'e', 'f'], ['a', 'e', 'g']],
#     cooldown=5
# )
# # # print(trigger.keys, type(trigger.keys))
# core_a = [ 'a', 'b', 'c', 'd']
# for k in core_a:
#     print(f'現在輸入：{k}')
#     trigger.check_key(k)
#     print(f'目前狀態：{trigger.state}')
#     time.sleep(0.5)