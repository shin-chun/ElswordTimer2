from gui.cooldown_window import CooldownWindow, CooldownState
from settings.common import *
from timer.timer_core import TimerCore
import threading
from manager.group_state_manager import GroupStateManager


class CooldownManager(QObject):
    start_timer_signal = Signal(str, object)  # 第二個參數用 object 接收 Enum
    def __init__(self, CooldownWindowClass):
        super().__init__()
        self.timer_cores: dict[str, TimerCore] = {}
        self.state = None
        self.CooldownWindowClass = CooldownWindowClass
        self.windows: dict[str, CooldownWindow] = {}
        self._timer: dict[str, QTimer] = {}
        self.moveToThread(QApplication.instance().thread())
        self.start_timer_signal.connect(self.start_timer)
        self.setup_shortcuts()
        self.group_manager = GroupStateManager()  # ✅ 新增群組管理器

        # 音效設置

    def add_timer(self, skill_name: str, cooldown_seconds: int, position=(300, 300)):
        if skill_name in self.windows:
            self.remove_timer(skill_name)

        window = self.CooldownWindowClass(skill_name, cooldown_seconds)
        window.move(*position)
        window.show()
        self.windows[skill_name] = window

    def start_timer(self, skill_name: str, state: CooldownState):
        window = self.get_window(skill_name)
        if not window:
            print(f"❌ 無法啟動技能「{skill_name}」，視窗不存在，略過啟動")
            return
        # 確保此方法在主執行緒執行
        if QThread.currentThread() != self.thread():
            # print(f"⚠️ 非主執行緒，透過 signal 轉移 start_timer({skill_name})")
            self.start_timer_signal.emit(skill_name, state)
            return

        existing_timer = self._timer.get(skill_name)
        if existing_timer and existing_timer.isActive():
            # print(f"⏳ Timer 已在運作中：{skill_name}，略過重啟")
            return

        # 建立視窗（如尚未存在）
        if skill_name not in self.windows:
            # print(f"🧊 尚未建立冷卻視窗：{skill_name}，自動建立")
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
        # print("✅ Timer started")
        # print("Manager thread:", self.thread())
        # print("Timer thread:", timer.thread())
        # print("Current thread:", QThread.currentThread())
        # print("Timer parent:", timer.parent())
        # print("Timer isActive:", timer.isActive())

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

            # ✅ 播放音效（用 thread 避免卡住 UI）
            threading.Thread(target=self._play_sound, daemon=True).start()

    def _play_sound(self):
        try:
            playsound("assets/sound/cooldown_complete.mp3")
        except Exception as e:
            print(f"❌ 播放音效失敗：{e}")

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
        print(skill_name, state)
        window = self.get_window(skill_name)
        if window:
            window.set_state(state)
        else:
            print(f"⚠️ 無法設定技能「{skill_name}」狀態，視窗不存在")

    def reset_all_cooldowns(self):
        print("🔄 F8 快捷鍵觸發：重置所有冷卻視窗")
        for skill_name, window in self.windows.items():
            window.set_remaining(window.cooldown_seconds)
            window.set_state(CooldownState.IDLE)

            # 停止 timer（如存在）
            if skill_name in self._timer:
                self._timer[skill_name].stop()
                self._timer[skill_name].deleteLater()
                del self._timer[skill_name]

            # 重置 TimerCore 狀態
            if skill_name in self.timer_cores:
                self.timer_cores[skill_name].reset()

            print(f"✅ 已重置：{skill_name}")

    def setup_shortcuts(self):
        reset_shortcut = QShortcut(QKeySequence("F8"), self)
        reset_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        reset_shortcut.activated.connect(self.reset_all_cooldowns)

    def close_all_windows(self):
        for window in self.windows.values():
            window.close()
        print("🛑 所有冷卻視窗已關閉")

    def set_timer_cores(self, timer_cores: dict[str, TimerCore]):
        self.timer_cores = timer_cores
        for core in self.timer_cores.values():
            core.bind_cooldown_manager(self)
            core.bind_group_manager(self.group_manager)  # ✅ 注入群組管理器

            print(f"🔗 已綁定 cooldown_manager 到 TimerCore「{core.name}」")

    def remove_timer(self, name: str):
        if name in self.windows:
            self.windows[name].close()
            del self.windows[name]
        if name in self._timer:
            self._timer[name].stop()
            self._timer[name].deleteLater()
            del self._timer[name]
        if name in self.timer_cores:
            del self.timer_cores[name]
