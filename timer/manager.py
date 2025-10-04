from timer.core import TimerCore
from gui.edit_window import EditWindow


class ButtonManager:
    def __init__(self):
        self.timers = []

    def create_edit_window(self):
        dialog = EditWindow(title='新增計時器')
        if dialog.exec():
            timer_name = dialog.name_input.text()
            print(f"新增的計時器名稱：{timer_name}")

    # def edit_timer(self, name, keys, cooldown, callback=None):
    #     timer = TimerCore(name=name, keys=keys, cooldown=cooldown, callback=callback)  # ✅ 關鍵
    #     print('pass')
    #
    # def save_file(self):
    #     print('pass')
    #
    # def delete_timer(self):
    #     print('pass')
    #
    # def reset_timer(self):
    #     print('pass')
    #
    # def import_config(self):
    #     print('pass')
    #
    # def input_key(self, key):
    #     print(f"🧩 TimerManager 收到鍵：{key}")
    #     for timer in self.timers:
    #         timer.input(key)


# class CooldownManager:
#     def update_countdown:
#
#     def update_label
