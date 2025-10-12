from gui.cooldown_window import CooldownWindow, CooldownState
from settings.common import *


class CooldownManager(QObject):
    start_timer_signal = Signal(str, object)  # 第二個參數用 object 接收 Enum

    def __init__(self, CooldownWindowClass):
        super().__init__()
        self.CooldownWindowClass = CooldownWindowClass
        self.windows: dict[str, CooldownWindow] = {}
        self._timer: dict[str, QTimer] = {}
        self.moveToThread(QApplication.instance().thread())
        self.start_timer_signal.connect(self.start_timer)

    def add_timer(self, skill_name: str, cooldown_seconds: int, position=(300, 300)):
        if skill_name in self.windows:
            self.remove_timer(skill_name)

        window = self.CooldownWindowClass(skill_name, cooldown_seconds)
        window.move(*position)
        window.show()
        self.windows[skill_name] = window

    def start_timer(self, skill_name: str, state: CooldownState):
        # 確保此方法在主執行緒執行
        if QThread.currentThread() != self.thread():
            print(f"⚠️ 非主執行緒，透過 signal 轉移 start_timer({skill_name})")
            self.start_timer_signal.emit(skill_name, state)
            return

        # 建立視窗（如尚未存在）
        if skill_name not in self.windows:
            print(f"🧊 尚未建立冷卻視窗：{skill_name}，自動建立")
            self.add_timer(skill_name, cooldown_seconds=5)

        window = self.windows[skill_name]
        window.set_state(state)
        window.set_remaining(window.cooldown_seconds)

        # 清除舊的 timer（如存在）
        if skill_name in self._timer:
            old_timer = self._timer.pop(skill_name)
            old_timer.stop()
            old_timer.deleteLater()

        # 建立新的 QTimer
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(partial(self._tick, skill_name))
        timer.start()
        self._timer[skill_name] = timer

        # 診斷印出
        print("✅ Timer started")
        print("Manager thread:", self.thread())
        print("Timer thread:", timer.thread())
        print("Current thread:", QThread.currentThread())
        print("Timer parent:", timer.parent())
        print("Timer isActive:", timer.isActive())

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