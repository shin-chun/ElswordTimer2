from settings.common import *
from gui.cooldown_window import CooldownState
from gui.edit_window import EditWindow
from timer.timer_core import TimerCore, Keys, Keys2


class MainWindowManager:
    def __init__(self, create_window_factory, event_list_widget, window):
        self.create_window_factory = create_window_factory
        self.list_widget = event_list_widget
        self.timers = {}
        self.window = window
        self.event_data_list = []  # 儲存每個事件的 dict

    def toggle_timer(self, running: bool):
        if running:
            self.show_all_cooldown_windows()
            print("✅ 已呼叫 show_all_cooldown_windows()")
        else:
            self.stop_all_timers_and_close_windows()

    def show_all_cooldown_windows(self):
        print(f"✅ timers 內容：{list(self.timers.keys())}")
        for name, timer in self.timers.items():
            timer.show_cooldown_window(state=CooldownState.SELECTED)  # ✅ 顯示冷卻視窗但不啟動

    def stop_all_timers_and_close_windows(self):
        for name, timer in self.timers.items():
            timer.stop_detection()
            timer.close_cooldown_window()

    def start_all_timers(self):
        for timer in self.timers.values():
            timer.start(CooldownState.SELECTED)

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
            self.timers[name] = TimerCore(
                name=name,
                keys=Keys(data["main_keys"][0], data["main_keys"][1], data["main_keys"][2]),
                keys2=Keys2(data["sub_keys"][0], data["sub_keys"][1], data["sub_keys"][2]),
                cooldown=data["duration"],
            )

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

        # ✅ 建立編輯視窗並載入原始資料
        dialog = EditWindow(parent=self.window, event_data=original_data)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_event_data()
            updated_name = updated_data.get("name", "")
            self.event_data_list[current_row] = updated_data  # ✅ 更新資料

            # ✅ 更新 list_widget 顯示
            main_keys = ','.join(updated_data.get("main_keys", []))
            sub_keys = ','.join(updated_data.get("sub_keys", []))
            duration = updated_data.get("duration")
            item_text = f'{updated_name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數: {duration}秒'
            self.list_widget.item(current_row).setText(item_text)

            # ✅ 更新 TimerCore 設定（如果名稱沒變就直接更新）
            if updated_name == original_name and updated_name in self.timers:
                self.timers[updated_name].update_config(
                    keys=Keys(*updated_data["main_keys"]),
                    keys2=Keys2(*updated_data["sub_keys"]),
                    cooldown=updated_data["duration"]
                )
            else:
                # ✅ 名稱有變更，需刪除舊的 TimerCore 並建立新的
                if original_name in self.timers:
                    del self.timers[original_name]
                self.timers[updated_name] = TimerCore(
                    name=updated_name,
                    keys=Keys(*updated_data["main_keys"]),
                    keys2=Keys2(*updated_data["sub_keys"]),
                    cooldown=updated_data["duration"]
                )

            if updated_name == original_name and updated_name in self.timers:
                self.timers[updated_name].update_config(
                    keys=Keys(*updated_data["main_keys"]),
                    keys2=Keys2(*updated_data["sub_keys"]),
                    cooldown=updated_data["duration"]
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

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.event_data_list, f, ensure_ascii=False, indent=2)
            print(f"儲存成功：{filepath}")
        except Exception as e:
            print(f"儲存失敗：{e}")

    def delete_timer(self):
        current_row = self.list_widget.currentRow()
        if current_row == -1:
            return  # 沒有選取項目就不處理

        reply = QMessageBox.question(
            self.list_widget,
            "確認刪除",
            "確定要刪除這個計時器嗎？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
        # 刪除列表項目
        self.list_widget.takeItem(current_row)
        # 刪除對應資料
        if current_row < len(self.event_data_list):
            del self.event_data_list[current_row]

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
                self.event_data_list = json.load(f)

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
            self.timers[name] = TimerCore(
                name=name,
                keys=Keys(*data["main_keys"]),
                keys2=Keys2(*data["sub_keys"]),
                cooldown=data["duration"]
            )


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
            timer.reset(duration)  # 假設你有定義 reset(duration) 方法
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
            timer.check_key(key)