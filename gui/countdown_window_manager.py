from gui.countdown_window import CountdownWindow

class CountdownWindowManager:
    def __init__(self):
        self.windows = []

    def cleanup(self):
        self.windows = [w for w in self.windows if w.isVisible()]

    def show_timer(self, name, duration):
        print(f"🪟 show_timer 被呼叫：{name}, {duration}")
        self.cleanup()
        window = CountdownWindow(name, duration)

        screen_geometry = window.screen().geometry()
        x = screen_geometry.width() - window.width() - 20
        y = screen_geometry.height() - window.height() - 20 - len(self.windows) * (window.height() + 10)
        window.move(x, y)

        self.windows.append(window)
        window.show()