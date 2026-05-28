import os
import re
import shutil

from dotenv import load_dotenv

load_dotenv()


PROJECT_DIR = os.getenv("PROJECT_DIR")
SOURCE_EXCEL_DIR = os.path.join(PROJECT_DIR, "company_excel")
TARGET_BASE_DIR = os.getenv("TARGET_BASE_DIR")


def get_leading_number(filename: str) -> int | None:
    match = re.match(r'^(\d+)', filename)
    if match:
        return int(match.group(1))
    return None


def find_target_folder_by_number(base_dir: str, number: int) -> str | None:
    if not os.path.isdir(base_dir):
        return None
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            match = re.match(r'^(\d+)', item)
            if match and int(match.group(1)) == number:
                return item_path
    return None


def move_files(region_name):
    if not os.path.isdir(SOURCE_EXCEL_DIR):
        print(f"Исходная папка не найдена: {SOURCE_EXCEL_DIR}")
        return

    if not os.path.isdir(TARGET_BASE_DIR):
        print(f"Целевая корневая папка не найдена: {TARGET_BASE_DIR}")
        return

    files = [f for f in os.listdir(SOURCE_EXCEL_DIR)
             if os.path.isfile(os.path.join(SOURCE_EXCEL_DIR, f)) and f.lower().endswith('.xlsx')]

    if not files:
        print("В папке company_excel нет Excel-файлов.")
        return

    moved_count = 0
    skipped_count = 0

    for filename in files:
        number = get_leading_number(filename)
        if number is None:
            print(f"⚠ Не удалось определить начальное число в файле: {filename} - пропущено")
            skipped_count += 1
            continue

        number_folder = find_target_folder_by_number(TARGET_BASE_DIR, number)
        if not number_folder:
            print(f"❌ Не найдена папка с числом {number} в {TARGET_BASE_DIR} для файла {filename}")
            skipped_count += 1
            continue

        region_folder = os.path.join(number_folder, region_name)
        if not os.path.isdir(region_folder):
            print(f"❌ В папке {os.path.basename(number_folder)} нет папки '{region_name}' для файла {filename}")
            skipped_count += 1
            continue

        source_path = os.path.join(SOURCE_EXCEL_DIR, filename)
        target_path = os.path.join(region_folder, filename)

        if os.path.exists(target_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(region_folder, f"{base}_{counter}{ext}")):
                counter += 1
            target_path = os.path.join(region_folder, f"{base}_{counter}{ext}")
            print(f"⚠ Файл {filename} уже существует, сохраняем как {os.path.basename(target_path)}")

        try:
            shutil.move(source_path, target_path)
            print(f"✅ Перемещён: {filename} -> {os.path.relpath(target_path, TARGET_BASE_DIR)}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Ошибка при перемещении {filename}: {e}")
            skipped_count += 1

    print(f"\nГотово! Перемещено: {moved_count}, пропущено/с ошибками: {skipped_count}")


if __name__ == "__main__":
    region = "Чувашия"
    move_files(region)
