import json
import os
import sys
from typing import Optional


class ScanCodeStore:
    def __init__(self, path: Optional[str] = None):
        self.path = path or self._default_path()
        self.mapping: dict[int, str] = self._load()

    def _default_path(self) -> str:
        """取得預設的 JSON 儲存路徑，支援打包後執行環境"""
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__))
        return os.path.join(base_dir, "scan_code_map.json")

    def _load(self) -> dict[int, str]:
        """載入 JSON 檔案並轉成 dict[int, str]"""
        if not os.path.exists(self.path):
            self._save({})
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return {int(k): v for k, v in json.load(f).items()}
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️ 無法解析掃描碼檔案：{e}")
            return {}

    def _save(self, data: dict[int, str]) -> None:
        """儲存 JSON 檔案"""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save(self) -> None:
        """手動儲存目前的 mapping"""
        self._save(self.mapping)

    def get(self, scan_code: int) -> Optional[str]:
        """取得掃描碼對應的鍵名"""
        return self.mapping.get(scan_code)

    def set(self, scan_code: int, key_name: str) -> None:
        """設定掃描碼對應鍵名並儲存"""
        self.mapping[scan_code] = key_name
        self.save()

    def has(self, scan_code: int) -> bool:
        """是否已存在此掃描碼"""
        return scan_code in self.mapping

    def all(self) -> dict[int, str]:
        """取得所有掃描碼對應表"""
        return dict(self.mapping)

    def delete(self, scan_code: int) -> None:
        """刪除某個掃描碼"""
        if scan_code in self.mapping:
            del self.mapping[scan_code]
            self.save()