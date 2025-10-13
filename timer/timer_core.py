from settings.common import *
from enum import Enum
from dataclasses import dataclass
from gui.cooldown_window import CooldownState
from manager.group_state_manager import GroupStateManager
from typing import Any, Optional



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
        self.timers = []
        self.group_name: Optional[str] = None
        self.group_manager: Optional[GroupStateManager] = None

    def bind_group(self, group_name: str):
        self.group_name = group_name
        self.debug(f"🔗 TimerCore「{self.name}」綁定群組：{group_name}")

    def bind_managers(self, group_manager, cooldown_manager):
        self.bind_group_manager(group_manager)
        self.bind_cooldown_manager(cooldown_manager)

    def bind_group_manager(self, group_manager: GroupStateManager):
        self.group_manager = group_manager
    #
    # def bind_manager(self, manager: Any):
    #     self.manager = manager
    #
    def bind_cooldown_manager(self, cooldown_manager: Any):
        self.cooldown_manager = cooldown_manager
        self.debug(f"🔗 TimerCore「{self.name}」已綁定 cooldown_manager")

    def check_key(self, key):
        print('冷卻管理器：', self.cooldown_manager, '群組管理器：', self.group_manager)
        if self.cooldown_manager is None or self.group_manager is None:
            self.debug(f"❌ TimerCore「{self.name}」尚未綁定管理器，忽略 key={key}")
            return
        print(f"🧪 準備呼叫 match_sequence，key={key}")
        print(f"🧪 keys: {self.keys}, keys2: {self.keys2}")
        print(f"🧪 keys.first_key={self.keys.first_key}, keys.second_key={self.keys.second_key}, keys.third_key={self.keys.third_key}")
        self.debug(f"🔍 準備進入 match_sequence，state={self.state}, key={key}")

        if not self.enabled:
            self.debug(f"🚫 TimerCore「{self.name}」未啟動，忽略 key={key}")
            return

        if self.state == TimerState.ACTIVE:
            self.debug(f"⏳ 技能「{self.name}」冷卻中，忽略 key={key}")
            return

        result = self.match_sequence(self.keys, key) or self.match_sequence(self.keys2, key)
        if not result:
            self.debug(f"❓ 技能「{self.name}」未匹配 key={key}，忽略")
            return

        # 群組鎖定邏輯
        if result == "LOCK":
            self.state = TimerState.LOCK
            self.cooldown_manager.set_state(self.name, CooldownState.LOCKED)
            self.debug(f"🔒 技能「{self.name}」進入鎖定狀態 key={key}")

            # ✅ 只有在鎖定時才重置同群組其他 timer
            if self.group_name:
                for timer in self.timers:
                    if timer is not self and timer.group_name == self.group_name:
                        self.debug(f"🔁 技能「{self.name}」鎖定後重置同群組：{timer.name}")
                        timer.reset_to_idle()

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
            if self.group_name:
                self.group_manager.release(self.group_name, self.name)

    def match_sequence(self, keys_obj, key) -> str | None:
        print(f"🧪 match_sequence() 被呼叫：{self.name}, key={key}")
        self.debug(f"🧪 match_sequence: key={key}, current_state={self.state}")
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

    def bind_all_timers(self, all_timers: list["TimerCore"]):
        self.timers = all_timers

    def reset_to_idle(self):
        print(f"🔁 [強制印出] 技能「{self.name}」被重置為 IDLE（原狀態：{self.state}）")

        self.debug(f"🔁 技能「{self.name}」被重置為 IDLE（原狀態：{self.state}）")
        self.state = TimerState.IDLE
        self.cooldown_manager.set_state(self.name, CooldownState.IDLE)

    # def lock_and_reset_others(self, locked_timer):
    #     print(locked_timer.keys.first_key)
    #     locked_key = locked_timer.keys.first_key
    #     for timer in self.timers:
    #         if timer is not locked_timer and timer.keys.first_key == locked_key:
    #             timer.reset_to_idle()