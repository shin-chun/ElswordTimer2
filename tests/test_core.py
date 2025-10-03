import time

class TriggerTimer:
    def __init__(self, keys, second_keys, cooldown, strick=None):
        self.keys = keys
        self.second_keys = second_keys
        self.cooldown = cooldown
        self.press_keys = []
        self.last_trigger_time = 0
        self.strick = strick

    def check_key(self, key):
        global pressed, mode_locked
        now = time.time()

        if now - self.last_trigger_time < self.cooldown:
            return False

        self.press_keys.append(key)
        press_keys = self.press_keys
        print(press_keys)

        for column in press_keys:
            for row in column:
                #step 1:事件啟動
                if row == self.keys:
                    mode_locked = None
                    print(f'開始判定：{press_keys}')
                    return
            #step 2：事件鎖定
            if self.keys in press_keys and self.keys in pressed:
                mode_locked = 'mkeys'

            elif self.keys in press_keys and self.second_keys in pressed and mode_locked is None:
                mode_locked = 'second_keys'

            for row in column:
                #step 3：觸發事件
                if mode_locked == 'keys':
                    for combo in self.keys:
                        print('觸發事件')
                        return
                elif mode_locked == 'second_keys':
                    for combo in self.second_keys:
                        print('second_keys')

# for k in ['a', 'b', 'e', 'f', 'a', 'b', 'd']:
#     on_key_press(k)