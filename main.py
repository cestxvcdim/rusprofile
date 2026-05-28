import time

from src.okved_base import get_okved_list, OKVED_LENGTH
from src.script import run_script, short_num

from utils.clean_empty_files import EXCEL_DIR, JSON_DIR, is_empty_excel, is_empty_json, clean_directory
from utils.move_files import move_files


def main(
        finance_revenue_from: str,
        finance_revenue_to: str,
        filename: str,
        regions: tuple[str, ...] | None = None,
        okved_many: bool = False
):
    if not okved_many:
        run_script(finance_revenue_from, finance_revenue_to, filename, regions)
    else:
        for ki in range(OKVED_LENGTH):
            print(f"{ki} KI цикл...")
            run_script(finance_revenue_from, finance_revenue_to, f"{ki} {filename}", regions, okved=get_okved_list(ki))
            if ki < OKVED_LENGTH - 1:
                time.sleep(5)


# "Республика Марий Эл": "12"
# "Республика Татарстан": "16"
# "Республика Чувашия": "21"
# "Кировская область": "43"
# "Московская область": "50"
# "Нижегородская область": "52"
# "Самарская область": "63"
# "Ульяновская область": "73"
# "Санкт-Петербург": "78"
# "Москва": ("77", "97")

if __name__ == '__main__':
    start = "100000000"  # Например, "20000000"
    end = "500000000"  # Например, "37670000"
    region = ("16",)  # Например, ("21",) - номер региона Чувашской Республики
    region_name = "Татарстан"  # Например, "Чувашская Республика"
    filename = f"{region_name} ({short_num(start)}-{short_num(end)})"

    # Run parser
    main(
        finance_revenue_from=start,
        finance_revenue_to=end,
        filename=filename,
        regions=region,
        okved_many=True,
    )

    # Clean files
    clean_directory(EXCEL_DIR, is_empty_excel)
    clean_directory(JSON_DIR, is_empty_json)

    # Move files
    move_files(region_name)
