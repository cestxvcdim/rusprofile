from src.okved_base import OKVED_ALL
from src.rus_profile import RusProfile


def short_num(number: str) -> str:
    length = len(number)
    if length < 4:
        return number
    if length < 7:
        return number[:(length-3)] + 'K'
    if length < 10:
        return number[:(length-6)] + 'M'
    if length < 13:
        return number[:(length-9)] + 'B'
    return number


def run_script(
        finance_revenue_from: str,
        finance_revenue_to: str,
        filename: str,
        regions: tuple[str, ...] | None = None,
        okved: list[str] | None = None,
):
    if int(finance_revenue_from) > int(finance_revenue_to):
        print("Минимальная выручка не может быть больше максимальной.")
        return

    if okved is None:
        okved = OKVED_ALL

    payload = {
        "sort": {
            "field": "finance_revenue",
            "order": "desc",
        },
        "state-1": True,
        "okved_strict": True,
        "okved": okved,
        "finance_revenue_from": finance_revenue_from,
        "finance_revenue_to": finance_revenue_to,
        "page": "1",
    }

    if regions is not None:
        payload["region"] = []
        for region in regions:
            payload["region"].append(region)

    rp = RusProfile()
    print("Идет получение данных...")
    all_data = rp.get_data(payload)
    print("Данные успешно получены.")

    rp.save_data_to_json(all_data, filename)
    rp.save_inn_to_excel(filename)

    print(f"ИНН сохранены в '{filename}.xlsx'.")
