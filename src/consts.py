SEARCH_URL = 'https://www.rusprofile.ru/ajax_auth.php?action=search_advanced'
MAIN_PAGE_URL = 'https://www.rusprofile.ru/search-advanced'

# Имитация запроса от браузера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.rusprofile.ru/search-advanced',
    'Origin': 'https://www.rusprofile.ru',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}
