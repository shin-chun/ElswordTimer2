from settings.common import *
from enum import Enum
from dataclasses import dataclass
from gui.cooldown_window import CooldownState
from typing import Any


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
        self.active = False
        self.debug_mode = False
        self.manager = None
        self.cooldown_manager = None  # 延遲注入
        self.enabled = False

    def bind_manager(self, manager: Any):
        self.manager = manager

    def bind_cooldown_manager(self, cooldown_manager: Any):
        self.cooldown_manager = cooldown_manager

    def check_key(self, key):
        if not self.enabled:
            self.debug(f"🚫 TimerCore「{self.name}」未啟動，忽略輸入 key={key}")
            return

        if self.state == TimerState.ACTIVE:
            self.debug(f"⏳ 技能「{self.name}」冷卻中，忽略輸入 key={key}")
            return

        result = self.match_sequence(self.keys, key) or self.match_sequence(self.keys2, key)
        if not result:
            self.debug(f"❓ 技能「{self.name}」未匹配 key={key}，忽略")
            return

        if result == "SELECT":
            self.state = TimerState.SELECT
            self.cooldown_manager.set_state(self.name, CooldownState.SELECTED)
            self.debug(f"🧊 技能「{self.name}」進入選擇狀態 key={key}")
        elif result == "LOCK":
            self.state = TimerState.LOCK
            self.cooldown_manager.set_state(self.name, CooldownState.LOCKED)
            self.debug(f"🔒 技能「{self.name}」進入鎖定狀態 key={key}")
        elif result == "TRIGGER":
            if not self.manager.has_timer(self.name):
                self.debug(f"⚠️ 技能「{self.name}」尚未建立冷卻視窗，略過觸發 key={key}")
                return
            self.state = TimerState.ACTIVE
            self.manager.start_timer_signal.emit(self.name, CooldownState.TRIGGERED)
            self.debug(f"🔥 技能「{self.name}」冷卻觸發 key={key}")

    def match_sequence(self, keys_obj, key) -> str | None:
        if keys_obj.third_key == key and not keys_obj.first_key and not keys_obj.second_key:
            return "TRIGGER"

        if key == keys_obj.first_key:
            return "SELECT"
        elif self.state == TimerState.SELECT and key == keys_obj.second_key:
            return "LOCK"
        elif self.state == TimerState.LOCK and key == keys_obj.third_key:
            return "TRIGGER"

        return None

    def update_config(self, keys: Keys, keys2: Keys2, cooldown: int):
        self.keys = keys
        self.keys2 = keys2
        self.cooldown = cooldown
        self.remaining = cooldown
        self.state = "IDLE"
        if self.manager:
            self.manager.update_timer(self.name, cooldown)
        print(f"🔄 TimerCore「{self.name}」已更新設定")

    def reset(self, cooldown=None):
        if cooldown is not None:
            self.cooldown = cooldown
        self.remaining = self.cooldown
        self.state = "IDLE"
        if self.manager:
            self.manager.reset_timer(self.name, self.cooldown)

    def debug(self, msg):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")

    def stop_detection(self):
        self.active = False
        print(f"🛑 TimerCore「{self.name}」已停止偵測")

