import requests
import time
import json
import pandas as pd

from random import randint
from consts import SEARCH_URL, MAIN_PAGE_URL, HEADERS


class RusProfile:
    def __init__(self):
        self.session = requests.Session()

    def update_csrf_token(self) -> None:
        try:
            self.session.get(MAIN_PAGE_URL, headers=HEADERS, timeout=10)
            csrf_token = self.session.cookies.get('__Host-csrf-token')
            if csrf_token:
                HEADERS['X-CSRF-Token'] = csrf_token
            time.sleep(1 + randint(1, 99) / 100)
        except Exception as e:
            print(f"Произошла ошибка при обновлении csrf_token: {e}")

    def _get_data(self, payload: dict):
        current_page = 1
        page_count = 1

        while current_page <= page_count:
            self.update_csrf_token()
            payload['page'] = str(current_page)
            print(f'Обработка {current_page} страницы...')
            try:
                response = self.session.post(SEARCH_URL, json=payload, headers=HEADERS, timeout=10)
                response.raise_for_status()
                response_data: dict = response.json()
                yield response_data

                pagination = response_data.get('pagination')
                if not pagination:
                    break

                page_count = pagination.get('page_count', 1)
                current_page = pagination.get('current', 1)

                current_page += 1

                time.sleep(8 + randint(1, 99) / 100)
            except Exception as e:
                print(e)

    def get_data(self, payload: dict) -> list:
        return list(self._get_data(payload))

    @staticmethod
    def save_data_to_json(data: list, filename: str) -> None:
        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_inn_list(filename: str) -> list[str]:
        with open(f'{filename}.json', 'r', encoding='utf-8') as f:
            loaded_data: dict = json.load(f)
            inn_list = []
            for page_data in loaded_data:
                companies = page_data.get('result')
                if companies:
                    for company in companies:
                        company_inn = company.get('inn')
                        if company_inn:
                            inn_list.append(company_inn)
            return inn_list

    def save_inn_to_excel(self, filename) -> None:
        df = pd.DataFrame({'ИНН': self.get_inn_list(filename)})
        df.to_excel(f'{filename}.xlsx', index=False)
