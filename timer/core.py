import time
from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class Keys:
    first_key: str
    second_key: str
    third_key: str


class TimerState(Enum):
    IDLE = "idle"
    SELECT = "select"
    LOCK = "locked"
    ACTIVE = "running"


class TimerCore:
    def __init__(self, name, keys: Keys, cooldown, callback=None):
        self.name = name
        self.keys = keys
        self.cooldown = cooldown
        self.callback = callback
        self.state = TimerState.IDLE

    def check_key(self, key):
        now = time.time()

        if self.keys.third_key == key and not self.keys.first_key and not self.keys.second_key:
            self.state = TimerState.ACTIVE
            self.trigger(self.cooldown)
            return

        if key == self.keys.first_key:
            self.state = TimerState.SELECT

        elif self.state == TimerState.SELECT and key == self.keys.second_key:
            self.state = TimerState.LOCK

        elif self.state == TimerState.LOCK and key == self.keys.third_key:
            self.state = TimerState.ACTIVE
            self.trigger(self.cooldown)

        # print(seq['keys'], type(seq['keys']))

    def trigger(self, cooldown):
        print(f"🚀 觸發技能：{self.name}，倒數 {cooldown} 秒")
        if self.callback:
            self.callback(self.name, cooldown)

    def reset(self, i):
        self.states[i] = 0
        self.last_times[i] = None

    def debug(self, msg):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")


# trigger = TimerCore(
#     name='test_trigger',
#     keys=Keys('a','b', 'c'),
#     # second_keys=[['a', 'e', 'f'], ['a', 'e', 'g']],
#     cooldown=5,
#     callback=callback
# )
# # print(trigger.keys, type(trigger.keys))
# core_a = ['a', 'b', 'e', 'c', 'f', 'a']
# for k in core_a:
#     print(f'現在輸入：{k}', type(k))
#     trigger.check_key(k)
#     time.sleep(0.5)