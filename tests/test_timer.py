from timer.timer_core import Timer

def mock_callback(name, duration):
    print(f"⏱️ {name} 倒數 {duration} 秒開始！")

timer = Timer(
    name="MultiSkill",
    sequences=[
        {"keys": ("a", "b", "c"), "duration": 30, "window": 2.0},
        {"keys": ("x", "y", "z"), "duration": 15, "window": 1.5},
        {"keys": (None, None, "q"), "duration": 10, "window": 0.5}
    ],
    callback=mock_callback
)

for key in ["a", "b", "c"]:
    timer.input(key)

for key in ["x", "y", "z"]:
    timer.input(key)

timer.input("q")  # 即時觸發