from gui.cooldown_window import CooldownWindow, CooldownState


class TimerManager:
    def __init__(self):
        self.windows = {}

    def add_timer(self, skill_name: str, cooldown_seconds: int, position=(300, 300)):
        if skill_name in self.windows:
            self.remove_timer(skill_name)

        window = CooldownWindow(skill_name, cooldown_seconds)
        x, y = position
        window.move(x, y)
        window.show()
        self.windows[skill_name] = window

    def start_timer(self, skill_name: str, state: CooldownState):
        if skill_name in self.windows:
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