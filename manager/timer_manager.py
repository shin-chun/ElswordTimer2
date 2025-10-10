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

    def remove_timer(self, skill_name: str):
        if skill_name in self.windows:
            self.windows[skill_name].close()
            del self.windows[skill_name]
