from settings.common import *
from gui.cooldown_window import CooldownState
from gui.edit_window import EditWindow
from timer.core import TimerCore, Keys, Keys2


class MainWindowManager:
    def __init__(self, create_window_factory, event_list_widget, window):
        self.create_window_factory = create_window_factory
        self.list_widget = event_list_widget
        self.window = window
        self.event_data_list = []  # 儲存每個事件的 dict

    def toggle_timer(self, running: bool):
        if running:
            self.start_all_timers()
        else:
            self.stop_all_timers()

    def start_all_timers(self):
        for timer in self.timers.values():
            timer.start(CooldownState.SELECTED)

    def open_edit_window(self):
        dialog = EditWindow(parent=self.window)
        dialog.exec()  # 或 dialog.show() 如果你要非模態


    def confirm_edit(self):
        dialog = EditWindow()
        if dialog.exec_() == QDialog.DialogCode.Accepted:
            data = dialog.get_event_data()
            name = data["name"]
            main_keys = ','.join(data["main_keys"])
            sub_keys = ','.join(data["sub_keys"])
            duration = str(data["duration"])  # ✅ 轉成字串
            item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys} , 秒數：{duration}'

            self.list_widget.addItem(item_text)
            self.event_data_list.append(data)  # ✅ 儲存原始資料

            print(data['duration'], type(data['duration']))

            keys_obj = TimerCore(
                name='test_trigger',
                keys=Keys(data['main_keys'][0], data['main_keys'][1], data['main_keys'][2]),
                keys2=Keys2(data['sub_keys'][0], data['sub_keys'][1], data['sub_keys'][2]),
                cooldown=data['duration'],
            )


    def edit_timer(self):
        current_row = self.list_widget.currentRow()
        if current_row == -1:
            return  # 沒有選取項目

        original_data = self.event_data_list[current_row]
        dialog = self.create_window_factory(original_data)  # ✅ 傳入原始資料

        # ✅ 載入原始資料到 dialog
        dialog.event_name_inputs[0].setText(original_data.get("name", ""))

        keys = original_data.get("main_keys", []) + original_data.get("sub_keys", [])
        for i, key in enumerate(keys):
            if i < len(dialog.key_labels):
                dialog.key_labels[i].setText(key)

        # ✅ 載入秒數（預設 10 秒）
        dialog.duration_input.setValue(original_data.get("duration", 10))

        if dialog.exec_() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_event_data()
            self.event_data_list[current_row] = updated_data  # ✅ 更新資料

            name = updated_data.get("name", "")
            main_keys = ','.join(updated_data.get("main_keys", []))
            sub_keys = ','.join(updated_data.get("sub_keys", []))
            duration = updated_data.get("duration")

            item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數: {duration}秒'
            self.list_widget.item(current_row).setText(item_text)

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
            QMessageBox.information(self.window, "匯入成功", f"已匯入：{filepath}")
        except Exception as e:
            QMessageBox.critical(self.window, "匯入失敗", f"錯誤：{e}")

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

        original_data = self.event_data_list[current_row]
        original_duration = original_data.get("duration", 10)  # 預設 10 秒

        # 重設邏輯：將 duration 設回原始值
        original_data["duration"] = original_duration

        # 更新顯示文字
        name = original_data.get("name", "")
        main_keys = ','.join(original_data.get("main_keys", []))
        sub_keys = ','.join(original_data.get("sub_keys", []))
        item_text = f'{name} → 主鍵: {main_keys}｜副鍵: {sub_keys}｜秒數：{original_duration}秒'
        self.list_widget.item(current_row).setText(item_text)

        QMessageBox.information(self.window, "已重置", f"計時器「{name}」已重置為 {original_duration} 秒")
