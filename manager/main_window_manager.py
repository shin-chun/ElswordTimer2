from settings.common import *
from gui.cooldown_window import CooldownState
from gui.edit_window import EditWindow
from timer.timer_core import Keys, Keys2, TimerCore
from timer.timer_factory import TimerFactory
from manager.cooldown_manager import CooldownManager


class MainWindowManager:
    def __init__(self, create_window_factory, event_list_widget, window, cooldown_manager):
        self.create_window_factory = create_window_factory
        self.list_widget = event_list_widget
        self.timers: dict[str, TimerCore] = {}
        self.window = window
        self.event_data_list = []  # 儲存每個事件的 dict
        self.cooldown_manager = cooldown_manager
        self.timer_factory = TimerFactory(self.cooldown_manager)
        self.cooldown_positions = {}  # name → (x, y)


    def toggle_timer(self, running: bool):
        for timer in self.timers.values():
            timer.enabled = running  # ✅ 修正錯誤：使用 running 而不是未定義的 enabled

        if running:
            self.show_all_cooldown_windows()
            print("✅ 已呼叫 show_all_cooldown_windows()")
        else:
            self.cooldown_positions = self.cooldown_manager.get_all_positions()
            print(f"📌 已記錄冷卻視窗位置：{self.cooldown_positions}")
            self.stop_all_timers_and_close_windows()

    def show_all_cooldown_windows(self):
        print(f"✅ timers 內容：{list(self.timers.keys())}")

        for name in self.timers:
            self.timers[name].reset()

            if not self.cooldown_manager.has_timer(name):
                position = self.cooldown_positions.get(name, (300, 300))
                cooldown = getattr(self.timers[name], "cooldown", 5)
                self.cooldown_manager.add_timer(name, cooldown, position=position)

            window = self.cooldown_manager.get_window(name)
            if window:
                self.cooldown_manager.set_state(name, CooldownState.IDLE)
                self.timers[name].bind_cooldown_manager(self.cooldown_manager)
                window.show()
                window.raise_()
                print(f"🪄 技能「{name}」視窗已顯示")
            else:
                print(f"⚠️ 技能「{name}」尚未建立視窗，略過顯示")

        print(f"🎯 共顯示 {len(self.timers)} 個冷卻視窗")

    def stop_all_timers_and_close_windows(self):
        for name, timer in self.timers.items():
            timer.stop_detection()
            timer.reset()  # ✅ 清除狀態與剩餘時間

            self.cooldown_manager.remove_timer(name)

    def start_all_timers(self):
        for name in self.timers:
            self.cooldown_manager.start_timer(name, CooldownState.IDLE)

    def open_edit_window(self):
        dialog = self.create_window_factory(parent=self.window)  # 建立編輯視窗
        result = dialog.exec()  # 顯示視窗（模態）

        if result == QDialog.DialogCode.Accepted:
            data = dialog.get_event_data()
            if not self.validate_event_data(data):
                return
            name = data["name"]
            main_keys = ','.join(data["main_keys"])
            sub_keys = ','.join(data["sub_keys"])
            duration = str(data["duration"])

            item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數：{duration}秒'
            self.list_widget.addItem(item_text)
            self.event_data_list.append(data)

            # ✅ 建立 TimerCore 並儲存
            self.timers[name] = self.timer_factory.create(
                name=name,
                keys=Keys(data["main_keys"][0], data["main_keys"][1], data["main_keys"][2]),
                keys2=Keys2(data["sub_keys"][0], data["sub_keys"][1], data["sub_keys"][2]),
                cooldown=data["duration"],
                callback=self.window.on_timer_triggered  # 如果你有 callback
            )
            # 綁定 cooldown_manager
            self.timers[name].bind_cooldown_manager(self.cooldown_manager)

            # 建立冷卻視窗
            self.cooldown_manager.add_timer(name, data["duration"])

    def validate_event_data(self, data):
        name = data.get("name", "").strip()
        if not name:
            QMessageBox.warning(self.window, "名稱未填", "請輸入事件名稱")
            return False
        if name in self.timers:
            QMessageBox.warning(self.window, "名稱重複", f"事件「{name}」已存在，請使用其他名稱")
            return False
        return True

    def edit_timer(self):
        current_row = self.list_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self.window, "未選取項目", "請先選取要編輯的計時器")
            return

        original_data = self.event_data_list[current_row]
        original_name = original_data.get("name", "")

        dialog = EditWindow(parent=self.window, event_data=original_data)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_event_data()
            updated_name = updated_data.get("name", "")
            self.event_data_list[current_row] = updated_data

            main_keys = ','.join(updated_data.get("main_keys", []))
            sub_keys = ','.join(updated_data.get("sub_keys", []))
            duration = updated_data.get("duration")
            item_text = f'{updated_name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數: {duration}秒'
            self.list_widget.item(current_row).setText(item_text)

            if updated_name == original_name and updated_name in self.timers:
                self.timers[updated_name].update_config(
                    keys=Keys(*updated_data["main_keys"]),
                    keys2=Keys2(*updated_data["sub_keys"]),
                    cooldown=updated_data["duration"]
                )
            else:
                if original_name in self.timers:
                    del self.timers[original_name]
                self.timers[updated_name] = self.timer_factory.create(
                    name=updated_name,
                    keys=Keys(*updated_data["main_keys"]),
                    keys2=Keys2(*updated_data["sub_keys"]),
                    cooldown=updated_data["duration"],
                    callback=self.window.on_timer_triggered
                )

    def save_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self.window,
            "儲存事件資料",
            "event_data.json",  # 預設檔名
            "JSON Files (*.json);;All Files (*)"
        )

        if not filepath:
            print("使用者取消儲存")
            return

        save_data = {
            "events": self.event_data_list,
            "positions": self.cooldown_positions
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print(f"儲存成功：{filepath}")
        except Exception as e:
            print(f"儲存失敗：{e}")

    def delete_timer_by_name_from_selection(self):
        current_row = self.list_widget.currentRow()
        if current_row == -1:
            return

        skill_name = self.event_data_list[current_row]["name"]
        self.delete_timer_by_name(skill_name)

        # ✅ 同步刪除 UI 與資料
        self.list_widget.takeItem(current_row)
        del self.event_data_list[current_row]

    def delete_timer_by_name(self, name: str):
        if name in self.timers:
            del self.timers[name]
        self.cooldown_manager.remove_timer(name)
        if name in self.cooldown_positions:
            del self.cooldown_positions[name]
        print(f"🗑️ 已從 MainWindowManager 刪除技能：{name}")


    def import_config_via_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self.window,
            "匯入事件資料",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not filepath:
            print("使用者取消匯入")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            # ✅ 讀取事件與位置資料
            self.event_data_list = loaded.get("events", [])
            self.cooldown_positions = {
                name: tuple(pos) for name, pos in loaded.get("positions", {}).items()
            }

            self.refresh_list()
            self.rebuild_timers_from_event_data()
            self.show_all_cooldown_windows()  # ✅ 可選：立即顯示冷卻視窗
            QMessageBox.information(self.window, "匯入成功", f"已匯入：{filepath}")
        except Exception as e:
            QMessageBox.critical(self.window, "匯入失敗", f"錯誤：{e}")

    def rebuild_timers_from_event_data(self):
        self.timers.clear()
        for data in self.event_data_list:
            name = data["name"]
            if not name.strip():
                continue  # 忽略空名稱

            self.timers[name] = self.timer_factory.create(
                name=name,
                keys=Keys(*data["main_keys"]),
                keys2=Keys2(*data["sub_keys"]),
                cooldown=data["duration"],
                callback=self.window.on_timer_triggered
            )

            # ✅ 還原冷卻視窗位置
            position = self.cooldown_positions.get(name, (300, 300))
            self.cooldown_manager.add_timer(name, data["duration"], position=position)

    def refresh_list(self):
        self.list_widget.clear()
        for data in self.event_data_list:
            name = data.get("name", "")
            main_keys = ','.join(data.get("main_keys", []))
            sub_keys = ','.join(data.get("sub_keys", []))
            duration = str(data.get("duration", 0))
            item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數：{duration}秒'
            self.list_widget.addItem(item_text)

    def reset_timer(self):
        current_row = self.list_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self.window, "未選取項目", "請先選取要重置的計時器")
            return

        data = self.event_data_list[current_row]
        name = data.get("name", "")
        duration = data.get("duration", 10)

        # ✅ 找到對應的 TimerCore 並重置
        timer = self.timers.get(name)
        if timer:
            timer.reset(duration)
            self.cooldown_manager.reset_timer(name, duration)  # 假設你有定義 reset(duration) 方法
            QMessageBox.information(self.window, "已重置", f"計時器「{name}」已重置為 {duration} 秒，狀態：IDLE")
        else:
            QMessageBox.warning(self.window, "找不到計時器", f"名稱為「{name}」的計時器不存在")

        # ✅ 更新 UI 顯示
        main_keys = ','.join(data.get("main_keys", []))
        sub_keys = ','.join(data.get("sub_keys", []))
        item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數：{duration}秒'
        self.list_widget.item(current_row).setText(item_text)

    def input_key(self, key: str):
        for timer in self.timers.values():
            if timer.enabled:
                try:
                    timer.check_key(key)
                except Exception as e:
                    print(f"❌ 技能觸發錯誤：{e}")

    def save_file_to_path(self, filepath):
        save_data = {
            "events": self.event_data_list,
            "positions": self.cooldown_positions
        }
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print(f"📝 已儲存設定到 {filepath}")
        except Exception as e:
            print(f"❌ 儲存失敗：{e}")
