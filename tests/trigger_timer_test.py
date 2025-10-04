import time

# from timer.test_timer import second_keys
# statistics

class TriggerTimer:
    def __init__(self, name, keys, second_keys, window, cooldown, strick=None):
        self.name = name
        self.keys = keys
        self.second_keys = second_keys
        self.window = window
        self.cooldown = cooldown
        self.press_keys = []
        self.index = 0
        self.last_trigger_time = 0
        self.strick = strick
        self.mode_locked = None

    def check_key(self, key):
        global pressed, mode_locked
        now = time.time()

        if now - self.last_trigger_time < self.cooldown:
            return False

        press_keys = self.press_keys.append(key)
        print(press_keys)
        for column in press_keys:
            for row in column:
                # step 1:事件啟動
                if row == self.keys:
                    mode_locked = None
                    print(f'開始判定：{press_keys}')
                    return
            # step 2：事件鎖定
            if self.keys in press_keys and self.keys in pressed:
                mode_locked = 'mkeys'

            elif self.keys in press_keys and self.second_keys in pressed and mode_locked is None:
                mode_locked = 'second_keys'

            for row in column:
                # step 3：觸發事件
                if mode_locked == 'keys':
                    for combo in self.keys:
                        print('觸發事件')
                        return
                elif mode_locked == 'second_keys':
                    for combo in self.second_keys:
                        print('second_keys')

    # for k in ['a', 'b', 'e', 'f', 'a', 'b', 'd']:
    #     on_key_press(k)

trigger = TriggerTimer(
    name='test_trigger',
    keys=[['a', 'b', 'c'], ['a', 'b', 'd']],
    second_keys=[['a', 'e', 'f'], ['a', 'e', 'g']],
    window=10,
    cooldown=5
)
# print(trigger.keys, type(trigger.keys))
array_a = ['a', 'b', 'e', 'c', 'f', 'a']
for k in array_a:
    print(f'現在輸入：{k}', type(k))
    trigger.check_key(k)
    time.sleep(0.5)