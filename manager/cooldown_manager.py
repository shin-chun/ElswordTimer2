from gui.cooldown_window import CooldownWindow, CooldownState
from settings.common import *


class CooldownManager(QObject):
    def __init__(self, CooldownWindowClass):
        super().__init__()
        self.CooldownWindowClass = CooldownWindowClass
        self.windows: dict[str, CooldownWindow] = {}
        self._timer: dict[str, QTimer] = {}
        self.state = CooldownState.IDLE

    def add_timer(self, skill_name: str, cooldown_seconds: int, position=(300, 300)):
        if skill_name in self.windows:
            self.remove_timer(skill_name)

        window = self.CooldownWindowClass(skill_name, cooldown_seconds)
        window.move(*position)
        window.show()
        self.windows[skill_name] = window

    def start_timer(self, skill_name: str, state: CooldownState):
        if skill_name not in self.windows:
            print(f"🧊 尚未建立冷卻視窗：{skill_name}，自動建立")
            self.add_timer(skill_name, cooldown_seconds=5)

        window = self.windows[skill_name]
        window.set_state(state)
        window.set_remaining(window.cooldown_seconds)

        if skill_name in self._timer:
            self._timer[skill_name].stop()
            self._timer[skill_name].deleteLater()

        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(lambda name=skill_name: self._tick(name))
        timer.start()
        self._timer[skill_name] = timer
        print(timer.isActive())

    def _tick(self, skill_name: str):
        print(f"⏱️ tick: {skill_name}")
        window = self.windows.get(skill_name)
        if not window:
            return

        window.decrement()
        if window.is_expired():
            self._timer[skill_name].stop()
            self._timer[skill_name].deleteLater()
            del self._timer[skill_name]
            window.set_state(CooldownState.IDLE)

    def reset_timer(self, skill_name: str, duration: int = None):
        window = self.windows.get(skill_name)
        if not window:
            return

        if duration is not None:
            window.cooldown_seconds = duration
        window.set_remaining(window.cooldown_seconds)
        window.set_state(CooldownState.IDLE)

        if skill_name in self._timer:
            self._timer[skill_name].stop()
            self._timer[skill_name].deleteLater()
            del self._timer[skill_name]

    def remove_timer(self, skill_name: str):
        if skill_name in self._timer:
            self._timer[skill_name].stop()
            self._timer[skill_name].deleteLater()
            del self._timer[skill_name]
        if skill_name in self.windows:
            self.windows[skill_name].close()
            del self.windows[skill_name]

    def has_timer(self, skill_name: str) -> bool:
        return skill_name in self.windows

    def get_window(self, skill_name: str) -> CooldownWindow | None:
        return self.windows.get(skill_name)

    def get_all_positions(self) -> dict[str, tuple[int, int]]:
        return {
            name: window.get_position()
            for name, window in self.windows.items()
        }

    def _update_position(self, name, pos):
        pass  # 可選擇即時更新或透過 callback 傳回

    def set_state(self, skill_name: str, state: CooldownState):
        if skill_name in self.windows:
            self.windows[skill_name].set_state(state)