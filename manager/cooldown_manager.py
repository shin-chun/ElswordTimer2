from gui.cooldown_window import CooldownWindow, CooldownState


class CooldownManager:
    def __init__(self):
        self.windows = {}

    def add_timer(self, skill_name: str, cooldown_seconds: int, position=(300, 300)):
        if skill_name in self.windows:
            self.remove_timer(skill_name)

        window = CooldownWindow(skill_name, cooldown_seconds)
        window.on_position_changed = lambda name, pos: self._update_position(name, pos)
        x, y = position
        window.move(x, y)
        window.show()
        self.windows[skill_name] = window
        # window.start(CooldownState.TRIGGERED)  # 或其他狀態

    def _update_position(self, name, pos):
        # 你可以選擇即時更新 MainWindowManager.cooldown_positions
        pass  # 或透過 callback 傳回

    def set_state(self, skill_name: str, state: CooldownState):
        if skill_name in self.windows:
            self.windows[skill_name].set_state(state)

    def start_timer(self, skill_name: str, state: CooldownState):
        if skill_name not in self.windows:
            print(f"🧊 尚未建立冷卻視窗：{skill_name}，自動建立")
            position = (300, 300)
            cooldown = 5  # 或從 self.timers[skill_name].cooldown 取得
            self.add_timer(skill_name, cooldown, position)

        self.windows[skill_name].start(state)

    def update_timer(self, skill_name: str, new_duration: int):
        if skill_name in self.windows:
            self.windows[skill_name].update_duration(new_duration)

    def reset_timer(self, skill_name: str, duration: int = None):
        if skill_name in self.windows:
            self.windows[skill_name].reset_display(duration)

    def remove_timer(self, skill_name: str):
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