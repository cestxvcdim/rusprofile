import os
import json
import openpyxl

from dotenv import load_dotenv

load_dotenv()


PROJECT_DIR = os.getenv("PROJECT_DIR")
EXCEL_DIR = os.path.join(PROJECT_DIR, "company_excel")
JSON_DIR = os.path.join(PROJECT_DIR, "company_json")


def is_empty_excel(file_path: str) -> bool:
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
    except Exception as e:
        print(f"Ошибка чтения Excel {file_path}: {e}")
        return False

    for sheet in wb.worksheets:
        max_row = sheet.max_row

        if max_row > 1:
            return False

    return True


def is_empty_json(file_path: str) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения JSON {file_path}: {e}")
        return False

    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict) and "result" in first_item:
            return first_item["result"] == []
    return False


def clean_directory(directory: str, checker) -> None:
    if not os.path.isdir(directory):
        print(f"Папка {directory} не найдена.")
        return

    print(f"\nОбработка папки {directory}:")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                if checker(file_path):
                    os.remove(file_path)
                    print(f"  Удалён: {filename}")
                else:
                    print(f"  Оставлен: {filename}")
            except Exception as e:
                print(f"  Ошибка при обработке {filename}: {e}")
