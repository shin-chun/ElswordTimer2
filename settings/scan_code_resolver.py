import json
import os

def get_scan_code_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "scan_code_map.json")

SCAN_CODE_FILE = get_scan_code_file_path()

def load_scan_code_map() -> dict[int, str]:
    if not os.path.exists(SCAN_CODE_FILE):
        with open(SCAN_CODE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(SCAN_CODE_FILE, "r", encoding="utf-8") as f:
        return {int(k): v for k, v in json.load(f).items()}

def save_scan_code_map(mapping: dict[int, str]) -> None:
    with open(SCAN_CODE_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4, ensure_ascii=False)