import time

class Timer:
    def __init__(self, name, sequences, callback=None):
        self.name = name
        self.sequences = sequences
        self.callback = callback
        self.states = [0] * len(sequences)
        self.last_times = [None] * len(sequences)

    def check_key(self, key):
        now = time.time()
        for i, seq in enumerate(self.sequences):
            ek, lk, tk = seq["keys"]
            duration = seq["duration"]
            window = seq["window"]

            if self.last_times[i] and now - self.last_times[i] > window:
                self.reset(i)

            state = self.states[i]

            if ek is None and lk is None and key == tk:
                self.trigger(duration)
                self.reset(i)
                continue

            if state == 0 and key == ek:
                self.states[i] = 1
                self.last_times[i] = now
            elif state == 1 and key == lk:
                self.states[i] = 2
                self.last_times[i] = now
            elif state == 2 and key == tk:
                self.trigger(duration)
                self.reset(i)
            else:
                self.reset(i)

        # print(seq['keys'], type(seq['keys']))

    def trigger(self, duration):
        print(f"🚀 觸發技能：{self.name}，倒數 {duration} 秒")
        if self.callback:
            self.callback(self.name, duration)

    def reset(self, i):
        self.states[i] = 0
        self.last_times[i] = None

    def debug(self, msg):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")