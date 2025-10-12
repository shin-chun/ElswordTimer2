from timer.timer_core import TimerCore, Keys, Keys2
from manager.cooldown_manager import CooldownManager


class TimerFactory:
    def __init__(self, manager: CooldownManager):
        self.manager = manager

    def create(self, name: str, keys: Keys, keys2: Keys2, cooldown: int, callback=None) -> TimerCore:
        core = TimerCore(name, keys, keys2, cooldown, callback=callback)
        core.bind_manager(self.manager)
        return core