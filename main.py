from okved_base import OKVED_ALL, get_okved_list
from rus_profile import RusProfile


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


def main(
        finance_revenue_from: str,
        finance_revenue_to: str,
        filename: str,
        regions: tuple[str, ...] | None = None,
        okved: list[str] = OKVED_ALL,
):
    if int(finance_revenue_from) > int(finance_revenue_to):
        print("Минимальная выручка не может быть больше максимальной.")
        return

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
    region = ("21",)  # Например, ("21",) - номер региона Чувашской Республики
    okved = get_okved_list(3)
    region_name = "Чувашская Республика"  # Например, "Чувашская Республика"
    filename = f"{region_name} ({short_num(start)}-{short_num(end)})"
    main(
        finance_revenue_from=start,
        finance_revenue_to=end,
        filename=filename,
        regions=region,
        okved=okved,
    )
