import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import argparse
import sys
import json
from urllib.parse import quote
import re

# --- Кэширование ---
CACHE_FILE = "wiki_cache.json"
_cache = {}

def load_cache():
    """Загружает кэш из файла."""
    global _cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                _cache = json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Предупреждение: Не удалось загрузить кэш из {CACHE_FILE}. Создаю новый.")
            _cache = {}

def save_cache():
    """Сохраняет кэш в файл."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_cache, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Ошибка при сохранении кэша: {e}")

# --- Функции для парсинга ---

def fetch_page_html(country_name, session, use_cache=True):
    """
    Получает HTML страницы страны из Википедии.
    Использует кэш, если возможно.
    """
    if use_cache and country_name in _cache:
        print(f"Загружаем '{country_name}' из кэша...")
        return _cache[country_name]

    url = f"https://en.wikipedia.org/wiki/{quote(country_name.replace(' ', '_'))}"
    print(f"Запрашиваю: {url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        html = response.text
        if use_cache:
            _cache[country_name] = html
        return html
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе для '{country_name}': {e}")
        return None

def extract_infobox_value(soup, label):
    """
    Ищет значение в инфобоксе Википедии по метке.
    Универсальная функция для поиска столицы, площади, населения.
    """
    infobox = soup.find('table', class_='infobox')
    if not infobox:
        return None

    # Ищем строку с нужной меткой
    row = infobox.find('th', string=lambda text: text and label in text)
    if not row:
        return None

    td = row.find_next('td')
    if td:
        text = td.get_text(separator=' ', strip=True)
        # Удаляем ссылки в квадратных скобках [1], [2] и т.д.
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return None

def clean_numeric(value_str):
    """
    Очищает строку с числом от запятых, пробелов и лишнего текста,
    оставляя только цифры.
    """
    if not value_str:
        return None
    # Удаляем все, кроме цифр
    cleaned = re.sub(r'[^\d]', '', value_str)
    return cleaned if cleaned else None

def extract_population(soup):
    """
    Специальная функция для извлечения населения, так как это сложнее.
    """
    # Ищем строку с Population
    population_row = soup.find('th', string=lambda text: text and 'Population' in text)
    if not population_row:
        return None
    
    td = population_row.find_next('td')
    if not td:
        return None
    
    text = td.get_text(separator=' ', strip=True)
    
    # Ищем числа в тексте (могут быть с запятыми)
    numbers = re.findall(r'[\d,]+', text)
    if numbers:
        # Берем самое большое число (обычно это общая численность)
        biggest = max(numbers, key=lambda x: len(x.replace(',', '')))
        return biggest.replace(',', '')
    return None

def parse_country_data(country_name, session, use_cache):
    """
    Основная функция для получения данных по одной стране.
    """
    html = fetch_page_html(country_name, session, use_cache)
    if not html:
        return None

    soup = BeautifulSoup(html, 'lxml')

    # 1. Извлечение столицы
    capital = extract_infobox_value(soup, 'Capital')
    if not capital:
        capital = extract_infobox_value(soup, 'Capital and largest city')

    # 2. Извлечение площади
    area_str = extract_infobox_value(soup, 'Area')
    area_cleaned = clean_numeric(area_str)

    # 3. Извлечение населения
    population_cleaned = extract_population(soup)

    return {
        'country': country_name,
        'city': capital if capital else 'N/A',
        'area': area_cleaned if area_cleaned else 'N/A',
        'population': population_cleaned if population_cleaned else 'N/A'
    }

# --- Основная программа ---
def main():
    parser = argparse.ArgumentParser(description='Парсинг данных о странах с Википедии.')
    parser.add_argument('-i', '--input', default='countries.txt',
                        help='Имя входного файла со списком стран (по умолчанию: countries.txt)')
    parser.add_argument('-o', '--output', default='countries_data.csv',
                        help='Имя выходного CSV файла (по умолчанию: countries_data.csv)')
    parser.add_argument('--no-cache', action='store_false', dest='use_cache',
                        help='Отключить использование кэша')
    parser.add_argument('--delay', type=float, default=1.0,
                        help='Задержка между запросами в секундах (по умолчанию: 1.0)')
    args = parser.parse_args()

    # Загружаем кэш
    if args.use_cache:
        load_cache()

    # Чтение списка стран из файла с автоматическим определением кодировки
    if not os.path.exists(args.input):
        print(f"Ошибка: Входной файл '{args.input}' не найден.")
        sys.exit(1)

    # Пробуем разные кодировки для чтения файла
    encodings_to_try = ['utf-8-sig', 'utf-16', 'cp1251', 'latin-1', 'utf-8']
    countries = None
    
    for enc in encodings_to_try:
        try:
            with open(args.input, 'r', encoding=enc) as f:
                countries = [line.strip() for line in f if line.strip()]
            print(f"Файл успешно прочитан в кодировке: {enc}")
            break
        except UnicodeDecodeError:
            continue
    
    if countries is None:
        print(f"Ошибка: Не удалось прочитать файл {args.input} ни в одной из кодировок")
        sys.exit(1)

    print(f"Найдено стран для обработки: {len(countries)}")
    print(f"Список стран: {', '.join(countries)}")

    # Сессия для повторного использования соединения
    with requests.Session() as session:
        results = []
        for i, country in enumerate(countries, 1):
            print(f"\n[{i}/{len(countries)}] Обработка: {country}")
            data = parse_country_data(country, session, args.use_cache)
            if data:
                results.append(data)
                print(f"  ✓ Найдено: Столица={data['city']}, Площадь={data['area']}, Население={data['population']}")
            else:
                print(f"  ✗ Не удалось получить данные для {country}")
                results.append({
                    'country': country,
                    'city': 'N/A',
                    'area': 'N/A',
                    'population': 'N/A'
                })

            # Пауза между запросами
            if i < len(countries):
                time.sleep(args.delay)

    # Сохраняем кэш
    if args.use_cache:
        save_cache()

    # Запись в CSV
    try:
        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['country', 'city', 'area', 'population']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow(row)

        print(f"\n✅ Готово! Данные сохранены в '{args.output}'")
        print(f"Обработано стран: {len(results)}")
        
        # Показываем первые несколько строк результата
        print("\nПервые 3 записи:")
        for row in results[:3]:
            print(f"  {row['country']}: {row['city']}, {row['area']} км², {row['population']} чел.")
            
    except IOError as e:
        print(f"Ошибка при записи CSV файла: {e}")

if __name__ == '__main__':
    main()